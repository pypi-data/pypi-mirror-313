#
# Copyright (c) Lightly AG and affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
from __future__ import annotations

from typing import Any

from torch.nn import Module

from lightly_train._models.feature_extractor import FeatureExtractor
from lightly_train._models.package import Package
from lightly_train._models.super_gradients.customizable_detector import (
    CustomizableDetectorFeatureExtractor,
)
from lightly_train._models.super_gradients.segmentation_module import (
    SegmentationModuleFeatureExtractor,
)
from lightly_train.errors import UnknownModelError


class SuperGradientsPackage(Package):
    name = "super_gradients"

    # Sadly SuperGradients doesn't expose a common interface for all models. We have to
    # define different feature extractors depending on the model types.
    _FEATURE_EXTRACTORS = [
        CustomizableDetectorFeatureExtractor,
        SegmentationModuleFeatureExtractor,
    ]

    @classmethod
    def list_model_names(cls) -> list[str]:
        try:
            from super_gradients.training import models  # type: ignore[import-untyped]
        except ImportError:
            return []
        model_names = {
            f"{cls.name}/{model_name}"
            for model_name, model_cls in models.ARCHITECTURES.items()
            if cls.is_supported_model_cls(model_cls=model_cls)
        }
        return sorted(model_names)

    @classmethod
    def is_supported_model(cls, model: Module) -> bool:
        return cls.is_supported_model_cls(model_cls=type(model))

    @classmethod
    def is_supported_model_cls(cls, model_cls: type[Module]) -> bool:
        return any(
            fe for fe in cls._FEATURE_EXTRACTORS if fe.is_supported_model_cls(model_cls)
        )

    @classmethod
    def get_model(
        cls, model_name: str, model_args: dict[str, Any] | None = None
    ) -> Module:
        try:
            from super_gradients.training import models
        except ImportError:
            raise ValueError(
                f"Cannot create model '{model_name}' because '{cls.name}' is not "
                "installed."
            )
        args = dict(num_classes=10)
        if model_args is not None:
            args.update(model_args)
        return models.get(model_name=model_name, **args)

    @classmethod
    def get_feature_extractor(cls, model: Module) -> FeatureExtractor:
        for fe in cls._FEATURE_EXTRACTORS:
            if fe.is_supported_model_cls(model_cls=type(model)):
                return fe(model)
        raise UnknownModelError(f"Unknown {cls.name} model: '{type(model)}'")


# Create singleton instance of the package. The singleton should be used whenever
# possible.
SUPER_GRADIENTS_PACKAGE = SuperGradientsPackage()
