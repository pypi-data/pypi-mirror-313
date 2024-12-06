#
# Copyright (c) Lightly AG and affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
from __future__ import annotations

from PIL.Image import Image as PILImage
from torch import Tensor

from lightly_train._transforms.to_tensor import ToTensor
from lightly_train._transforms.to_tensor import torchvision_transforms as T


class EmbeddingTransform:
    def __init__(
        self,
        image_size: int | tuple[int, int],
        mean: tuple[float, float, float],
        std: tuple[float, float, float],
    ):
        self.transform = T.Compose(
            [
                T.Resize(size=image_size),
                ToTensor(),
                T.Normalize(mean=mean, std=std),
            ]
        )

    def __call__(self, image: PILImage) -> Tensor:
        return self.transform(image)
