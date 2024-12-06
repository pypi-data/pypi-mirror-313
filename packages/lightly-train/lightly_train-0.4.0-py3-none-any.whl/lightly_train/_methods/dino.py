#
# Copyright (c) Lightly AG and affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
from __future__ import annotations

import copy
from typing import Any, Literal

import torch
from lightly.loss import DINOLoss
from lightly.models.modules.heads import DINOProjectionHead
from lightly.models.utils import update_momentum
from lightly.transforms import DINOTransform as LightlyDINOTransform
from lightly.utils import optim
from lightly.utils.scheduler import cosine_schedule
from pydantic import Field
from torch import Tensor
from torch.nn import Flatten
from torch.optim import Optimizer

from lightly_train import _scaling
from lightly_train._configs.validate import no_auto
from lightly_train._methods.method import Method, TrainingStepResult
from lightly_train._methods.method_args import MethodArgs
from lightly_train._models.embedding_model import EmbeddingModel
from lightly_train._optim.adamw_args import AdamWArgs
from lightly_train._optim.optimizer_args import OptimizerArgs
from lightly_train._optim.optimizer_type import OptimizerType
from lightly_train._optim.sgd_args import SGDArgs
from lightly_train._optim.trainable_modules import TrainableModules
from lightly_train._scaling import IMAGENET_SIZE, ScalingInfo
from lightly_train._transforms.transform import (
    MethodTransform,
    MethodTransformArgs,
    RandomResizeArgs,
)
from lightly_train.types import MultiViewBatch


class DINOArgs(MethodArgs):
    """Args for DINO method for ImageNet dataset."""

    # projection head
    hidden_dim: int = 2048
    bottleneck_dim: int = 256
    output_dim: int | Literal["auto"] = "auto"
    student_freeze_last_layer_epochs: int = 1
    batch_norm: bool = False
    norm_last_layer: bool = True
    # loss
    teacher_temp: float | Literal["auto"] = "auto"
    warmup_teacher_temp: float | Literal["auto"] = "auto"
    warmup_teacher_temp_epochs: int | Literal["auto"] = "auto"
    student_temp: float = 0.1
    center_momentum: float = 0.9
    # momentum
    momentum_start: float | Literal["auto"] = "auto"
    momentum_end: float = 1.0
    # weight decay
    weight_decay_start: float | Literal["auto"] = "auto"
    weight_decay_end: float | Literal["auto"] = "auto"

    def resolve_auto(
        self, scaling_info: ScalingInfo, optimizer_args: OptimizerArgs
    ) -> None:
        dataset_size = scaling_info.dataset_size

        if self.output_dim == "auto":
            # Default output dim of 65536 is too large for small datasets.
            self.output_dim = _scaling.get_bucket_value(
                input=dataset_size,
                buckets=[
                    (20_000, 1024),
                    (50_000, 2048),
                    (100_000, 4096),
                    (200_000, 16384),
                    (500_000, 32768),
                    (float("inf"), 65536),
                ],
            )

        if self.teacher_temp == "auto":
            # Default teacher temperature of 0.07 is too high for small datasets. Lower
            # temperature results in stronger sharpening which avoids collapse to uniform
            # distribution.
            self.teacher_temp = _scaling.interpolate(
                dataset_size,
                input_start=20_000,
                input_end=IMAGENET_SIZE,
                value_start=0.02,
                value_end=0.07,
                round_ndigits=2,
            )

        if self.warmup_teacher_temp == "auto":
            self.warmup_teacher_temp = min(
                self.teacher_temp,
                _scaling.interpolate(
                    input=self.teacher_temp,
                    input_start=0.02,
                    input_end=0.07,
                    value_start=0.02,
                    value_end=0.04,
                    round_ndigits=2,
                ),
            )

        if self.warmup_teacher_temp_epochs == "auto":
            # Default warmup teacher temperature epochs of 30 is too high when training
            # for only a few total epochs. Have the warmup period be 30% of all epochs,
            # but with a maximum of 30 epochs.
            self.warmup_teacher_temp_epochs = int(
                _scaling.interpolate(
                    scaling_info.epochs,
                    input_start=0,
                    input_end=100,
                    value_start=0,
                    value_end=30,
                )
            )

        if self.momentum_start == "auto":
            # Default momentum start of 0.996 is too high for small datasets. Lower momentum
            # results in slower updates of the teacher model. This is important because with
            # high momentum (fast changing teacher) and a small dataset, the initial
            # training epochs become unstable.
            self.momentum_start = _scaling.interpolate(
                dataset_size,
                input_start=20_000,
                input_end=IMAGENET_SIZE,
                value_start=0.99,
                value_end=0.996,
                round_ndigits=3,
            )

        if isinstance(optimizer_args, (AdamWArgs, SGDArgs)):
            weight_decay = optimizer_args.weight_decay
        else:
            raise ValueError(f"Unsupported optimizer_args type: {type(optimizer_args)}")
        if self.weight_decay_start == "auto":
            self.weight_decay_start = weight_decay
        if self.weight_decay_end == "auto":
            self.weight_decay_end = weight_decay


class DINOTransformArgs(MethodTransformArgs):
    # TODO: Authors recommend to use different scales for convnets than
    # transformers. We should add a check for the model type and use the appropriate
    # scales accordingly.
    # https://github.com/facebookresearch/dino#resnet-50-and-other-convnets-trainings
    random_resize: RandomResizeArgs = Field(
        default_factory=lambda: RandomResizeArgs(min_scale=0.14)
    )
    # Strict is set to False because OmegaConf does not support parsing tuples from the
    # CLI. Setting strict to False allows Pydantic to convert lists to tuples.
    local_view_size: tuple[int, int] = Field(default=(96, 96), strict=False)
    local_view_resize: RandomResizeArgs = Field(
        default_factory=lambda: RandomResizeArgs(min_scale=0.05, max_scale=0.14)
    )
    n_local_views: int = 6


class DINOTransform(MethodTransform):
    def __init__(self, transform_args: DINOTransformArgs):
        self.transform_args = transform_args
        # Typing: LightlyDINOTransform is a Callable[[PILImage], list[Tensor]]
        self.transform = LightlyDINOTransform(
            global_crop_size=transform_args.image_size,  # type: ignore[arg-type]
            global_crop_scale=(
                transform_args.random_resize.min_scale,
                transform_args.random_resize.max_scale,
            ),
            local_crop_size=transform_args.local_view_size,  # type: ignore[arg-type]
            local_crop_scale=(
                transform_args.local_view_resize.min_scale,
                transform_args.local_view_resize.max_scale,
            ),
            n_local_views=transform_args.n_local_views,
            hf_prob=transform_args.random_flip.horizontal_prob,
            vf_prob=transform_args.random_flip.vertical_prob,
            random_gray_scale=transform_args.random_gray_scale,
            normalize=(
                None
                if transform_args.normalize is None
                else transform_args.normalize.to_dict()
            ),
        )  # type: ignore[assignment]

    @staticmethod
    def transform_args_cls() -> type[DINOTransformArgs]:
        return DINOTransformArgs


class DINOAdamWArgs(AdamWArgs):
    lr: float = 0.0005
    weight_decay: float = 0.04


class DINOSGDArgs(SGDArgs):
    lr: float = 0.03
    weight_decay: float = 0.0001


class DINO(Method):
    def __init__(
        self,
        method_args: DINOArgs,
        optimizer_args: OptimizerArgs,
        embedding_model: EmbeddingModel,
        global_batch_size: int,
    ):
        super().__init__(
            method_args=method_args,
            optimizer_args=optimizer_args,
            embedding_model=embedding_model,
            global_batch_size=global_batch_size,
        )
        self.method_args = method_args
        self.teacher_embedding_model = embedding_model
        self.teacher_projection_head = DINOProjectionHead(
            input_dim=self.teacher_embedding_model.embed_dim,
            hidden_dim=method_args.hidden_dim,
            bottleneck_dim=method_args.bottleneck_dim,
            output_dim=no_auto(method_args.output_dim),
            batch_norm=method_args.batch_norm,
            freeze_last_layer=0,
            norm_last_layer=method_args.norm_last_layer,
        )
        self.student_embedding_model = copy.deepcopy(self.teacher_embedding_model)
        self.student_projection_head = DINOProjectionHead(
            input_dim=self.student_embedding_model.embed_dim,
            hidden_dim=method_args.hidden_dim,
            bottleneck_dim=method_args.bottleneck_dim,
            output_dim=no_auto(method_args.output_dim),
            batch_norm=method_args.batch_norm,
            freeze_last_layer=method_args.student_freeze_last_layer_epochs,
            norm_last_layer=method_args.norm_last_layer,
        )
        self.flatten = Flatten(start_dim=1)
        self.criterion = DINOLoss(
            output_dim=no_auto(method_args.output_dim),
            teacher_temp=no_auto(method_args.teacher_temp),
            warmup_teacher_temp=no_auto(method_args.warmup_teacher_temp),
            warmup_teacher_temp_epochs=no_auto(method_args.warmup_teacher_temp_epochs),
            student_temp=method_args.student_temp,
            center_momentum=method_args.center_momentum,
        )

    def training_step_impl(
        self, batch: MultiViewBatch, batch_idx: int
    ) -> TrainingStepResult:
        momentum = cosine_schedule(
            step=self.trainer.global_step,
            max_steps=self.trainer.estimated_stepping_batches,
            start_value=no_auto(self.method_args.momentum_start),
            end_value=self.method_args.momentum_end,
        )
        update_momentum(
            self.student_embedding_model, self.teacher_embedding_model, m=momentum
        )
        update_momentum(
            self.student_projection_head, self.teacher_projection_head, m=momentum
        )

        views = batch[0]
        global_views = torch.cat(views[:2])
        local_views = torch.cat(views[2:])

        x_teacher = self._forward_teacher(global_views)
        x_student = torch.cat(
            [self._forward_student(global_views), self._forward_student(local_views)]
        )

        loss = self.criterion(
            teacher_out=x_teacher.chunk(2),
            student_out=x_student.chunk(len(views)),
            epoch=self.current_epoch,
        )

        return TrainingStepResult(loss=loss)

    @torch.no_grad()
    def _forward_teacher(self, x: Tensor) -> Tensor:
        x = self.teacher_embedding_model(x)
        x = self.flatten(x)
        x = self.teacher_projection_head(x)
        return x

    def _forward_student(self, x: Tensor) -> Tensor:
        x = self.student_embedding_model(x)
        x = self.flatten(x)
        x = self.student_projection_head(x)
        return x

    @staticmethod
    def method_args_cls() -> type[DINOArgs]:
        return DINOArgs

    @staticmethod
    def optimizer_args_cls(
        optim_type: OptimizerType | Literal["auto"],
    ) -> type[OptimizerArgs]:
        classes: dict[OptimizerType | Literal["auto"], type[OptimizerArgs]] = {
            "auto": DINOSGDArgs,
            OptimizerType.ADAMW: DINOAdamWArgs,
            OptimizerType.SGD: DINOSGDArgs,
        }
        return classes.get(optim_type, Method.optimizer_args_cls(optim_type=optim_type))

    def trainable_modules(self) -> TrainableModules:
        return TrainableModules(
            modules=[self.student_embedding_model, self.student_projection_head]
        )

    def configure_gradient_clipping(
        self,
        optimizer: Optimizer,
        gradient_clip_val: int | float | None = None,
        gradient_clip_algorithm: str | None = None,
    ) -> None:
        self.clip_gradients(
            optimizer=optimizer,
            gradient_clip_val=3.0,
            gradient_clip_algorithm="norm",
        )
        self.student_projection_head.cancel_last_layer_gradients(self.current_epoch)

    def on_before_optimizer_step(self, optimizer: Optimizer, *args: Any) -> None:
        weight_decay = cosine_schedule(
            step=self.trainer.global_step,
            max_steps=self.trainer.estimated_stepping_batches,
            start_value=self.method_args.weight_decay_start,
            end_value=self.method_args.weight_decay_end,
        )
        optim.update_param_groups(
            optimizer, updates=[{"name": "params", "weight_decay": weight_decay}]
        )

    @staticmethod
    def transform_cls() -> type[MethodTransform]:
        return DINOTransform
