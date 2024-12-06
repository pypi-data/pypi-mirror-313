#
# Copyright (c) Lightly AG and affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
from __future__ import annotations

import re
from typing import Any

from torch.nn import Module
from torchvision import models as torchvision_models

from lightly_train._models.feature_extractor import FeatureExtractor
from lightly_train._models.package import Package
from lightly_train._models.torchvision.convnext import ConvNeXtFeatureExtractor
from lightly_train._models.torchvision.resnet import ResNetFeatureExtractor
from lightly_train._models.torchvision.torchvision import TorchvisionFeatureExtractor
from lightly_train.errors import UnknownModelError


class TorchvisionPackage(Package):
    name = "torchvision"

    _FEATURE_EXTRACTORS = [ConvNeXtFeatureExtractor, ResNetFeatureExtractor]

    @classmethod
    def list_model_names(cls) -> list[str]:
        regex_str = "|".join(
            f"({fe._torchvision_model_name_pattern})" for fe in cls._FEATURE_EXTRACTORS
        )
        pattern = re.compile(pattern=regex_str)
        model_names = {
            f"{cls.name}/{model_name}"
            for model_name in torchvision_models.list_models()
            if pattern.match(model_name)
        }
        return sorted(model_names)

    @classmethod
    def is_supported_model(cls, model: Module) -> bool:
        return type(model) in cls._model_cls_to_extractor_cls()

    @classmethod
    def get_model(
        cls, model_name: str, model_args: dict[str, Any] | None = None
    ) -> Module:
        args = dict()
        if model_args is not None:
            args.update(model_args)
        return torchvision_models.get_model(model_name, **args)

    @classmethod
    def get_feature_extractor(cls, model: Module) -> FeatureExtractor:
        feature_extractor_cls = cls._model_cls_to_extractor_cls().get(type(model))
        if feature_extractor_cls is not None:
            return feature_extractor_cls(model)
        raise UnknownModelError(f"Unknown torchvision model: '{model}'")

    @classmethod
    def _model_cls_to_extractor_cls(
        cls,
    ) -> dict[type[Module], type[TorchvisionFeatureExtractor]]:
        module_to_cls = {}
        for feature_extractor_cls in cls._FEATURE_EXTRACTORS:
            for model_cls in feature_extractor_cls._torchvision_models:
                module_to_cls[model_cls] = feature_extractor_cls
        return module_to_cls


# Create singleton instance of the package. The singleton should be used whenever
# possible.
TORCHVISION_PACKAGE = TorchvisionPackage()
