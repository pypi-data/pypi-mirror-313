#
# Copyright (c) Lightly AG and affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
from __future__ import annotations

import logging
import os
import pprint
from pathlib import Path
from typing import Any, Literal

from pytorch_lightning.accelerators.accelerator import Accelerator
from pytorch_lightning.accelerators.cpu import CPUAccelerator
from pytorch_lightning.accelerators.cuda import CUDAAccelerator
from pytorch_lightning.accelerators.mps import MPSAccelerator
from pytorch_lightning.strategies.strategy import Strategy
from torch.nn import Module

from lightly_train.types import PathLike

logger = logging.getLogger(__name__)


def get_checkpoint_path(checkpoint: PathLike) -> Path:
    checkpoint_path = Path(checkpoint).resolve()
    logger.debug(f"Making sure checkpoint '{checkpoint_path}' exists.")
    if not checkpoint_path.exists():
        raise FileNotFoundError(f"Checkpoint '{checkpoint_path}' does not exist!")
    if not checkpoint_path.is_file():
        raise ValueError(f"Checkpoint '{checkpoint_path}' is not a file!")
    return checkpoint_path


def get_out_path(out: PathLike, overwrite: bool) -> Path:
    out_path = Path(out).resolve()
    logger.debug(f"Checking if output path '{out_path}' exists.")
    if out_path.exists():
        if not overwrite:
            raise ValueError(
                f"Output '{out_path}' already exists! Set overwrite=True to overwrite "
                "the file."
            )
        if not out_path.is_file():
            raise ValueError(f"Output '{out_path}' is not a file!")
    return out_path


def get_accelerator(
    accelerator: str | Accelerator,
) -> str | Accelerator:
    logger.debug(f"Getting accelerator for '{accelerator}'.")
    if accelerator != "auto":
        # User specified an accelerator, return it.
        return accelerator

    # Default to CUDA if available.
    if CUDAAccelerator.is_available():
        logger.debug("CUDA is available, defaulting to CUDA.")
        return CUDAAccelerator()
    elif MPSAccelerator.is_available():
        logger.debug("MPS is available, defaulting to MPS.")
        return MPSAccelerator()
    else:
        logger.debug("CUDA and MPS are not available, defaulting to CPU.")
        return CPUAccelerator()


def _get_rank() -> int | None:
    """Get the rank of the current process.

    Copied from https://github.com/Lightning-AI/pytorch-lightning/blob/06a8d5bf33faf0a4f9a24207ae77b439354350af/src/lightning/fabric/utilities/rank_zero.py#L39-L49
    """
    # SLURM_PROCID can be set even if SLURM is not managing the multiprocessing,
    # therefore LOCAL_RANK needs to be checked first
    rank_keys = ("RANK", "LOCAL_RANK", "SLURM_PROCID", "JSM_NAMESPACE_RANK")
    for key in rank_keys:
        rank = os.environ.get(key)
        if rank is not None:
            return int(rank)
    # None to differentiate whether an environment variable was set at all
    return None


def is_rank_zero() -> bool:
    """Check if the current process is running on the first device."""
    local_rank = _get_rank()
    return local_rank == 0 or local_rank is None


def get_out_dir(out: PathLike, resume: bool, overwrite: bool) -> Path:
    out_dir = Path(out).resolve()
    logger.debug(f"Checking if output directory '{out_dir}' exists.")
    if out_dir.exists():
        if not out_dir.is_dir():
            raise ValueError(f"Output '{out_dir}' is not a directory!")

        dir_not_empty = any(out_dir.iterdir())

        if dir_not_empty and (not (resume or overwrite)) and is_rank_zero():
            raise ValueError(
                f"Output '{out_dir}' is not empty! Set overwrite=True to overwrite the "
                "directory or resume=True to resume training."
            )
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir


def pretty_format_args(
    args: dict[str, Any], indent: int = 2, width: int = 200, compact: bool = True
) -> str:
    args = sanitize_config_dict(args)

    return pprint.pformat(args, indent=indent, width=width, compact=compact)


def sanitize_config_dict(args: dict[str, Any]) -> dict[str, Any]:
    """Replace classes with their names in the train config dictionary."""
    if isinstance(args.get("model"), Module):
        args["model"] = args["model"].__class__.__name__
    if isinstance(args.get("accelerator"), Accelerator):
        args["accelerator"] = args["accelerator"].__class__.__name__
    if isinstance(args.get("strategy"), Strategy):
        args["strategy"] = args["strategy"].__class__.__name__
    return args


def get_num_workers(
    num_workers: int | Literal["auto"], num_devices_per_node: int
) -> int:
    """Returns the number of workers for the dataloader.

    The number of workers are per dataloader. Every device has its own dataloader.
    """
    if num_workers == "auto":
        num_cpus_per_device = _get_num_cpus_per_device(
            num_devices_per_node=num_devices_per_node
        )
        if num_cpus_per_device is None:
            num_workers = 8
        else:
            # Leave 1 CPU for the main process on every device
            num_workers = max(num_cpus_per_device - 1, 0)
    return num_workers


def _get_num_cpus_per_device(num_devices_per_node: int) -> int | None:
    """Returns the number of available CPUs per device."""
    if _is_slurm():
        cpus_per_task = os.getenv("SLURM_CPUS_PER_TASK")
        logger.debug(f"SLURM_CPUS_PER_TASK: {cpus_per_task}")
        if cpus_per_task and isinstance(cpus_per_task, str):
            cpu_count = int(cpus_per_task)
        else:
            cpu_count = None
    else:
        cpu_count = os.cpu_count()
        if cpu_count is not None:
            cpu_count = cpu_count // num_devices_per_node
    return cpu_count


def _is_slurm() -> bool:
    return "SLURM_JOB_ID" in os.environ
