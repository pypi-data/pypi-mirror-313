#
# Copyright (c) Lightly AG and affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
from __future__ import annotations

import os
from collections.abc import Iterable, Sequence, Set
from pathlib import Path
from typing import Callable, NewType

from PIL import Image, ImageFile
from PIL.Image import Image as PILImage
from torch import Tensor
from torch.utils.data import Dataset

ImageFile.LOAD_TRUNCATED_IMAGES = True

ImageFilename = NewType("ImageFilename", str)


class ImageDataset(Dataset):
    def __init__(
        self,
        image_dir: Path,
        image_filenames: Sequence[ImageFilename],
        transform: Callable[[PILImage], PILImage | Tensor] | None = None,
    ):
        self.image_dir = image_dir
        self.image_filenames = image_filenames
        self.transform = transform

    def __getitem__(self, idx: int) -> tuple[PILImage | Tensor, ImageFilename]:
        filename = self.image_filenames[idx]
        image = Image.open(self.image_dir / filename).convert("RGB")
        if self.transform is not None:
            return self.transform(image), filename
        return image, filename

    def __len__(self) -> int:
        return len(self.image_filenames)


def list_image_filenames(image_dir: Path) -> Iterable[ImageFilename]:
    """List image filenames relative to `image_dir` recursively.

    Args:
        image_dir:
            The root directory to scan for images.

    Returns:
        An iterable of image filenames relative to `image_dir`.
    """
    return (
        ImageFilename(str(fpath.relative_to(image_dir)))
        for fpath in _get_image_filepaths(image_dir=image_dir)
    )


def _get_image_filepaths(image_dir: Path) -> Iterable[Path]:
    extensions = _pil_supported_image_extensions()
    for root, _, files in os.walk(image_dir, followlinks=True):
        root_path = Path(root)
        for file in files:
            fpath = root_path / file
            if fpath.suffix.lower() in extensions:
                yield fpath


def _pil_supported_image_extensions() -> Set[str]:
    return {
        ex
        for ex, format in Image.registered_extensions().items()
        if format in Image.OPEN
    }
