#
# Copyright (c) Lightly AG and affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
from pathlib import Path

import pytest
import torch

from lightly_train._models.ultralytics.ultralytics import UltralyticsFeatureExtractor
from lightly_train._models.ultralytics.ultralytics_package import UltralyticsPackage

try:
    from ultralytics import RTDETR, YOLO
except ImportError:
    # We do not use pytest.importorskip on module level because it makes mypy unhappy.
    pytest.skip("ultralytics is not installed", allow_module_level=True)


class TestUltralyticsPackage:
    @pytest.mark.parametrize(
        "model_name, supported",
        [
            ("ultralytics/yolov5s.yaml", True),
            ("ultralytics/yolov5s.pt", False),  # No pretrained checkpoint available.
            ("ultralytics/yolov6s.yaml", True),
            ("ultralytics/yolov6s.pt", False),  # No pretrained checkpoint available.
            ("ultralytics/yolov8s.yaml", True),
            ("ultralytics/yolov8s.pt", True),
            ("ultralytics/yolov10s.pt", False),  # Not yet supported.
        ],
    )
    def test_list_model_names(self, model_name: str, supported: bool) -> None:
        model_names = UltralyticsPackage.list_model_names()
        assert (model_name in model_names) is supported

    def test_is_supported_model__true(self) -> None:
        model = YOLO("yolov8s.yaml")
        assert UltralyticsPackage.is_supported_model(model)

    def test_is_supported_model__false(self) -> None:
        model = RTDETR("rtdetr-l.yaml")
        assert not UltralyticsPackage.is_supported_model(model)

    @pytest.mark.parametrize(
        "model_name",
        ["yolov8s.pt", "yolov8s.yaml"],
    )
    def test_get_model(self, model_name: str) -> None:
        model = UltralyticsPackage.get_model(model_name=model_name)
        assert isinstance(model, YOLO)

    def test_get_feature_extractor(self) -> None:
        model = YOLO("yolov8s.yaml")
        fe = UltralyticsPackage.get_feature_extractor(model=model)
        assert isinstance(fe, UltralyticsFeatureExtractor)

    def test_export_model(self, tmp_path: Path) -> None:
        out = tmp_path / "model.pt"
        model = YOLO("yolov8n.yaml")

        UltralyticsPackage.export_model(model=model, out=out)
        model_exported = YOLO(out)

        # Check that parameters are the same.
        assert len(list(model.parameters())) == len(list(model_exported.parameters()))
        for (name, param), (name_exp, param_exp) in zip(  # type: ignore[call-overload]
            model.named_parameters(), model_exported.named_parameters()
        ):
            assert name == name_exp
            assert param.dtype == param_exp.dtype
            assert param.requires_grad == param_exp.requires_grad
            assert torch.allclose(param, param_exp, rtol=1e-3, atol=1e-4)

        # Check module states.
        assert len(list(model.modules())) == len(list(model_exported.modules()))
        for (name, module), (name_exp, module_exp) in zip(  # type: ignore[call-overload]
            model.named_modules(), model_exported.named_modules()
        ):
            assert name == name_exp
            if isinstance(module, YOLO):
                # Main module is always in training mode.
                assert module.training
                assert module_exp.training
            else:
                # Pretrained models are loaded differently by ultralytics. Their modules
                # are by default in eval mode.
                assert module.training  # Model from yaml is in training mode
                assert not module_exp.training  # Model from checkpoint is in eval mode
