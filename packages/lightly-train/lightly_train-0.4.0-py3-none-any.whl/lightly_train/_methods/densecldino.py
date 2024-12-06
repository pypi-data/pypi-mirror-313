#
# Copyright (c) Lightly AG and affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
"""DenseCLDINO

Implementation based on mixture of DenseCL and DINO. The method reuses all model parts
from DINO with the following differences:
* There is an extra local projection head
* There is an extra local loss term
* The local loss is calculated on features matched based on DenseCL
"""

from __future__ import annotations

import copy
from typing import Literal

import torch
from lightly.loss import DINOLoss
from lightly.models import utils
from lightly.models.modules.heads import DINOProjectionHead
from lightly.models.utils import update_momentum
from lightly.utils.scheduler import cosine_schedule
from torch import Tensor
from torch.nn import AdaptiveAvgPool2d, Module
from torch.optim import Optimizer

from lightly_train._methods.densecl import no_auto
from lightly_train._methods.dino import DINOAdamWArgs, DINOArgs, DINOTransform
from lightly_train._methods.method import Method, TrainingStepResult
from lightly_train._models.embedding_model import EmbeddingModel
from lightly_train._optim.optimizer_args import OptimizerArgs
from lightly_train._optim.optimizer_type import OptimizerType
from lightly_train._optim.trainable_modules import TrainableModules
from lightly_train._transforms.transform import MethodTransform
from lightly_train.types import MultiViewBatch


class DenseCLDINOArgs(DINOArgs):
    """Args for DenseCLDINO method for ImageNet dataset."""

    # loss
    lambda_: float = 0.5  # Default from DenseCLArgs


class DenseCLDINOEncoder(Module):
    def __init__(
        self,
        embedding_model: EmbeddingModel,
        hidden_dim: int,
        bottleneck_dim: int,
        output_dim: int,
        batch_norm: bool,
        freeze_last_layer: int,
        norm_last_layer: bool,
    ) -> None:
        super().__init__()
        self.embedding_model = embedding_model
        self.local_projection_head = DINOProjectionHead(
            input_dim=embedding_model.embed_dim,
            hidden_dim=hidden_dim,
            bottleneck_dim=bottleneck_dim,
            output_dim=output_dim,
            batch_norm=batch_norm,
            freeze_last_layer=freeze_last_layer,
            norm_last_layer=norm_last_layer,
        )
        self.global_projection_head = DINOProjectionHead(
            input_dim=embedding_model.embed_dim,
            hidden_dim=hidden_dim,
            bottleneck_dim=bottleneck_dim,
            output_dim=output_dim,
            batch_norm=batch_norm,
            freeze_last_layer=freeze_last_layer,
            norm_last_layer=norm_last_layer,
        )
        self.pool = AdaptiveAvgPool2d((1, 1))

    def forward(self, x: Tensor) -> tuple[Tensor, Tensor, Tensor]:
        # B = batch size, C = number of channels, H = image height, W = image width, D = output_dim
        # (B, C, H, W)
        features = self.embedding_model(x, pool=False)
        # (B, C, H, W) -> (B, C, 1, 1) -> (B, C)
        global_proj = self.pool(features).flatten(start_dim=1)
        # (B, C) -> (B, D)
        global_proj = self.global_projection_head(global_proj)
        # (B, C, H, W) -> (B, C, H*W) -> (B, H*W, C)
        features = features.flatten(start_dim=2).permute(0, 2, 1)
        # (B, H*W, C) -> (B, H*W, D)
        local_proj = self.local_projection_head(features)
        # Return: (B, H*W, C), (B, D), (B, H*W, D)
        return features, global_proj, local_proj


# NOTE(11/24, Guarin): DenseCLDINO is disabled because it is very different from the
# original DenseCL implementation. In particular, it doesn't use pooled local features
# as negative examples.
class DenseCLDINO(Method):
    def __init__(
        self,
        method_args: DenseCLDINOArgs,
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
        self.teacher_encoder = DenseCLDINOEncoder(
            embedding_model=embedding_model,
            hidden_dim=method_args.hidden_dim,
            bottleneck_dim=method_args.bottleneck_dim,
            output_dim=no_auto(method_args.output_dim),
            batch_norm=method_args.batch_norm,
            freeze_last_layer=0,
            norm_last_layer=method_args.norm_last_layer,
        )
        self.student_encoder = DenseCLDINOEncoder(
            embedding_model=copy.deepcopy(embedding_model),
            hidden_dim=method_args.hidden_dim,
            bottleneck_dim=method_args.bottleneck_dim,
            output_dim=no_auto(method_args.output_dim),
            batch_norm=method_args.batch_norm,
            freeze_last_layer=method_args.student_freeze_last_layer_epochs,
            norm_last_layer=method_args.norm_last_layer,
        )

        self.local_criterion = DINOLoss(
            output_dim=no_auto(method_args.output_dim),
            teacher_temp=no_auto(method_args.teacher_temp),
            warmup_teacher_temp=method_args.warmup_teacher_temp,
            warmup_teacher_temp_epochs=method_args.warmup_teacher_temp_epochs,
            student_temp=method_args.student_temp,
            center_momentum=method_args.center_momentum,
        )
        self.global_criterion = DINOLoss(
            output_dim=no_auto(method_args.output_dim),
            teacher_temp=no_auto(method_args.teacher_temp),
            warmup_teacher_temp=method_args.warmup_teacher_temp,
            warmup_teacher_temp_epochs=method_args.warmup_teacher_temp_epochs,
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
        update_momentum(self.student_encoder, self.teacher_encoder, m=momentum)

        views = batch[0]
        global_views = torch.cat(views[:2])
        local_views = torch.cat(views[2:])

        # Forward teacher.
        with torch.no_grad():
            (
                features_teacher,
                global_proj_teacher,
                local_proj_teacher,
            ) = self.teacher_encoder(global_views)

        # Forward student.
        (
            global_features_student,
            global_global_proj_student,
            global_local_proj_student,
        ) = self.student_encoder(global_views)
        _, local_global_proj_student, _ = self.student_encoder(local_views)

        # Global loss (normal DINO loss).
        global_proj_student = torch.cat(
            [global_global_proj_student, local_global_proj_student], dim=0
        )
        global_loss = self.global_criterion(
            teacher_out=global_proj_teacher.chunk(2),
            student_out=global_proj_student.chunk(len(views)),
            epoch=self.current_epoch,
        )

        # Local loss (Dense matching + DINO loss). This is only calculated on the
        # global views as matching global with local views is tricky due to the
        # different number of features.
        global_local_proj_student = utils.select_most_similar(
            features_teacher, global_features_student, global_local_proj_student
        )

        local_proj_teacher = local_proj_teacher.flatten(end_dim=1)
        global_local_proj_student = global_local_proj_student.flatten(end_dim=1)

        local_loss = self.local_criterion(
            teacher_out=local_proj_teacher.chunk(2),
            student_out=global_local_proj_student.chunk(2),
            epoch=self.current_epoch,
        )

        # Final loss.
        lambda_ = self.method_args.lambda_
        loss = (1 - lambda_) * global_loss + lambda_ * local_loss

        return TrainingStepResult(loss=loss)

    @staticmethod
    def method_args_cls() -> type[DenseCLDINOArgs]:
        return DenseCLDINOArgs

    @staticmethod
    def optimizer_args_cls(
        optim_type: OptimizerType | Literal["auto"],
    ) -> type[OptimizerArgs]:
        if optim_type in ("auto", OptimizerType.ADAMW):
            return DINOAdamWArgs
        return Method.optimizer_args_cls(optim_type=optim_type)

    def trainable_modules(self) -> TrainableModules:
        return TrainableModules(modules=[self.student_encoder])

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
        self.student_encoder.local_projection_head.cancel_last_layer_gradients(
            self.current_epoch
        )
        self.student_encoder.global_projection_head.cancel_last_layer_gradients(
            self.current_epoch
        )

    @staticmethod
    def transform_cls() -> type[MethodTransform]:
        return DINOTransform
