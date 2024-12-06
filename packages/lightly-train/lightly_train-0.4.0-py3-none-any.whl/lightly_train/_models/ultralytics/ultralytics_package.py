#
# Copyright (c) Lightly AG and affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
from __future__ import annotations

import copy
import logging
from pathlib import Path
from typing import Any

from torch.nn import Module

from lightly_train._models.feature_extractor import FeatureExtractor
from lightly_train._models.package import Package
from lightly_train._models.ultralytics.ultralytics import (
    UltralyticsFeatureExtractor,
)

logger = logging.getLogger(__name__)


class UltralyticsPackage(Package):
    name = "ultralytics"

    @classmethod
    def list_model_names(cls) -> list[str]:
        try:
            from ultralytics.nn import tasks
            from ultralytics.utils import downloads
        except ImportError:
            return []

        # We currently only support models that have a backbone ending with an SPPF
        # layer. See ultralytics/cfg/models for different architectures.
        supported_models = {"yolov5", "yolov6", "yolov8"}

        # These models are downloaded from the ultralytics repository.
        pretrained_models = {
            f"{model_name}.pt"
            for model_name in downloads.GITHUB_ASSETS_STEMS
            if any(model_name.startswith(model) for model in supported_models)
        }

        # These models are instantiated from their yaml configuration files.
        untrained_models = {
            f"{model_name}{scale}.yaml"
            for model_name in supported_models
            for scale in ["n", "s", "m", "l", "x"]
        }
        untrained_models.update(
            {model_name.replace(".pt", ".yaml") for model_name in pretrained_models}
        )
        # Check that the model configs are available. Ultralytics doesn't provide
        # a list of available models/configs.
        for model_name in list(untrained_models):
            try:
                # This only loads the model config, not the model itself.
                tasks.yaml_model_load(model_name)
            except FileNotFoundError:
                untrained_models.remove(model_name)

        model_names = pretrained_models.union(untrained_models)
        model_names = {f"{cls.name}/{model_name}" for model_name in model_names}
        return sorted(model_names)

    @classmethod
    def is_supported_model(cls, model: Module) -> bool:
        try:
            from ultralytics import YOLO
        except ImportError:
            return False
        return isinstance(model, YOLO)

    @classmethod
    def get_model(
        cls, model_name: str, model_args: dict[str, Any] | None = None
    ) -> Module:
        try:
            from ultralytics import YOLO
        except ImportError:
            raise ValueError(
                f"Cannot create model '{model_name}' because '{cls.name}' is not "
                "installed."
            )
        args = {} if model_args is None else model_args
        model = YOLO(model=model_name, **args)
        return model

    @classmethod
    def get_feature_extractor(cls, model: Module) -> FeatureExtractor:
        return UltralyticsFeatureExtractor(model=model)

    @classmethod
    def export_model(cls, model: Module, out: Path) -> None:
        try:
            from ultralytics import YOLO
        except ImportError:
            raise ValueError(
                f"Cannot export model because '{cls.name}' is not installed."
            )
        if not isinstance(model, YOLO):
            raise ValueError(f"Model must be of type 'YOLO', but is '{type(model)}'.")
        export_model = copy.deepcopy(model)
        if export_model.ckpt is None:
            export_model.ckpt = {}
        export_model.save(out)


# Create singleton instance of the package. The singleton should be used whenever
# possible.
ULTRALYTICS_PACKAGE = UltralyticsPackage()
