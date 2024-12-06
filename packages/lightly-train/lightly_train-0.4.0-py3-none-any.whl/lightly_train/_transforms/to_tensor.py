#
# Copyright (c) Lightly AG and affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
import torch
from torch import Tensor

from lightly_train._transforms.transform import Transform

try:
    from torchvision.transforms import v2 as torchvision_transforms

    _TRANSFORMS_V2 = True

except ImportError:
    from torchvision import transforms as torchvision_transforms

    _TRANSFORMS_V2 = False


import logging

logger = logging.getLogger(__name__)


def ToTensor() -> Transform[Tensor]:
    T = torchvision_transforms
    if _TRANSFORMS_V2 and hasattr(T, "ToImage") and hasattr(T, "ToDtype"):
        logger.debug("Using torchvision v2 transforms for ToTensor.")
        # v2.transforms.ToTensor is deprecated and will be removed in the future.
        # This is the new recommended way to convert a PIL Image to a tensor since
        # torchvision v0.16.
        # See also https://github.com/pytorch/vision/blame/33e47d88265b2d57c2644aad1425be4fccd64605/torchvision/transforms/v2/_deprecated.py#L19
        T = torchvision_transforms
        return T.Compose([T.ToImage(), T.ToDtype(dtype=torch.float32, scale=True)])
    else:
        logger.debug("Using torchvision v1 transforms for ToTensor.")
        return T.ToTensor()
