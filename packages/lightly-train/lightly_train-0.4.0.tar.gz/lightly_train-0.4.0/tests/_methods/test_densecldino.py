#
# Copyright (c) Lightly AG and affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
from lightly_train._methods.densecldino import DenseCLDINOArgs
from lightly_train._optim.adamw_args import AdamWArgs
from lightly_train._scaling import ScalingInfo


class TestDenseCLDINOArgs:
    def test_resolve_auto(self) -> None:
        args = DenseCLDINOArgs()
        scaling_info = ScalingInfo(dataset_size=20_000, epochs=100)
        args.resolve_auto(scaling_info=scaling_info, optimizer_args=AdamWArgs())
        assert not args.has_auto()
