#
# Copyright (c) Lightly AG and affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
from __future__ import annotations

from typing import (
    Generic,
    Protocol,
    Type,
    TypeVar,
)

from lightly.transforms.utils import IMAGENET_NORMALIZE
from PIL.Image import Image as PILImage
from pydantic import Field
from torch import Tensor

from lightly_train._configs.config import PydanticConfig


class RandomResizeArgs(PydanticConfig):
    min_scale: float = 0.08
    max_scale: float = 1.0


class RandomFlipArgs(PydanticConfig):
    horizontal_prob: float = 0.5
    vertical_prob: float = 0.0


class NormalizeArgs(PydanticConfig):
    # Strict is set to False because OmegaConf does not support parsing tuples from the
    # CLI. Setting strict to False allows Pydantic to convert lists to tuples.
    mean: tuple[float, float, float] = Field(
        default=(
            IMAGENET_NORMALIZE["mean"][0],
            IMAGENET_NORMALIZE["mean"][1],
            IMAGENET_NORMALIZE["mean"][2],
        ),
        strict=False,
    )
    std: tuple[float, float, float] = Field(
        default=(
            IMAGENET_NORMALIZE["std"][0],
            IMAGENET_NORMALIZE["std"][1],
            IMAGENET_NORMALIZE["std"][2],
        ),
        strict=False,
    )

    def to_dict(self) -> dict:
        return {
            "mean": self.mean,
            "std": self.std,
        }

    @classmethod
    def from_dict(cls, config: dict) -> NormalizeArgs:
        return cls(
            mean=config["mean"],
            std=config["std"],
        )


class MethodTransformArgs(PydanticConfig):
    # Strict is set to False because OmegaConf does not support parsing tuples from the
    # CLI. Setting strict to False allows Pydantic to convert lists to tuples.
    image_size: tuple[int, int] = Field(default=(224, 224), strict=False)
    random_resize: RandomResizeArgs = Field(default_factory=RandomResizeArgs)
    random_flip: RandomFlipArgs = Field(default_factory=RandomFlipArgs)
    random_gray_scale: float = 0.2
    normalize: NormalizeArgs = Field(default_factory=NormalizeArgs)


_T = TypeVar("_T", covariant=True)


class Transform(Generic[_T], Protocol):
    # `image` is a positional only argument because naming of the argument differs
    # between lightly, v1, and v2 transforms.
    def __call__(self, image: PILImage, /) -> _T: ...


class MethodTransform:
    transform_args: MethodTransformArgs
    transform: Transform[list[Tensor]]

    def __init__(self, transform_args: MethodTransformArgs):
        raise NotImplementedError

    def __call__(self, image: PILImage, /) -> list[Tensor]:
        return self.transform(image)

    @staticmethod
    def transform_args_cls() -> Type[MethodTransformArgs]:
        raise NotImplementedError
