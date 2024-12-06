#
# Copyright (c) Lightly AG and affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
from __future__ import annotations

from typing import Type

from lightly_train._methods.densecl import DenseCL
from lightly_train._methods.dino import DINO
from lightly_train._methods.method import Method
from lightly_train._methods.simclr import SimCLR


def list_methods() -> list[str]:
    """Lists all available self-supervised learning methods.

    See the documentation for more information: https://docs.lightly.ai/train/stable/methods/
    """
    return sorted(_method_name_to_cls().keys())


def get_method_cls(method: str | Method) -> Type[Method]:
    if isinstance(method, Method):
        return method.__class__
    method_cls = _method_name_to_cls().get(method)
    if method_cls is not None:
        return method_cls
    else:
        raise ValueError(
            f"Method '{method}' is unknown. Available methods are: {list_methods()}"
        )


def _method_name_to_cls() -> dict[str, Type[Method]]:
    return {
        m.__name__.lower(): m
        for m in [
            DenseCL,
            # DenseCLDINO,  # Disable for now.
            DINO,
            SimCLR,
        ]
    }
