#
# Copyright (c) Lightly AG and affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
import pytest

try:
    import timm
except ImportError:
    # We do not use pytest.importorskip on module level because it makes mypy unhappy.
    pytest.skip("timm is not installed", allow_module_level=True)

from lightly_train._models.timm.timm_package import TIMMPackage

from ...helpers import DummyCustomModel


class TestTIMMPackage:
    def test_is_model(self) -> None:
        model = timm.create_model("resnet18")
        assert TIMMPackage.is_supported_model(model)

    def test_is_model__false(self) -> None:
        model = DummyCustomModel()
        assert not TIMMPackage.is_supported_model(model)
