#
# Copyright (c) Lightly AG and affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
from typing import Type

import pytest

from lightly_train._methods import method_helpers
from lightly_train._methods.densecl import DenseCL
from lightly_train._methods.dino import DINO
from lightly_train._methods.method import Method
from lightly_train._methods.simclr import SimCLR

from .. import helpers


@pytest.mark.parametrize(
    "method, expected",
    [
        ("densecl", DenseCL),
        # ("densecldino", DenseCLDINO), # Disable for now.
        ("dino", DINO),
        ("simclr", SimCLR),
        (helpers.get_method(), SimCLR),
    ],
)
def test_get_method_cls(method: str, expected: Type[Method]) -> None:
    assert method_helpers.get_method_cls(method=method) == expected


def test_list_methods() -> None:
    assert method_helpers.list_methods() == [
        "densecl",
        # "densecldino", # Disable for now.
        "dino",
        "simclr",
    ]
