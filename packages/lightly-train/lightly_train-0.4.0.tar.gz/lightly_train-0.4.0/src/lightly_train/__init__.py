#
# Copyright (c) Lightly AG and affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#

# Disable beta transforms warning by torchvision.
# See https://stackoverflow.com/questions/77279407
# TODO(Philipp, 09/24): Remove this once the warning is removed.
import torchvision

torchvision.disable_beta_transforms_warning()

from lightly_train._commands.embed import embed
from lightly_train._commands.export import ModelFormat, ModelPart, export
from lightly_train._commands.train import train
from lightly_train._embedding.embedding_format import EmbeddingFormat
from lightly_train._methods.method_helpers import list_methods
from lightly_train._models.package_helpers import list_model_names as list_models

__all__ = [
    "embed",
    "EmbeddingFormat",
    "export",
    "list_methods",
    "list_models",
    "ModelFormat",
    "ModelPart",
    "train",
]

__version__ = "0.4.0"
