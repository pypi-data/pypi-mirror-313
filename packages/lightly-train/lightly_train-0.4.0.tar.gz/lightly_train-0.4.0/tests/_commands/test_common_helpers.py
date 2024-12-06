#
# Copyright (c) Lightly AG and affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Literal

import pytest
from pytest_mock import MockerFixture
from pytorch_lightning.accelerators.cpu import CPUAccelerator
from pytorch_lightning.strategies.ddp import DDPStrategy
from torch.nn import Module
from torchvision import models

from lightly_train._commands import common_helpers


def test_get_checkpoint_path(tmp_path: Path) -> None:
    out_file = tmp_path / "file.ckpt"
    out_file.touch()
    assert common_helpers.get_checkpoint_path(checkpoint=out_file) == out_file


def test_get_checkpoint_path__non_existing(tmp_path: Path) -> None:
    out_dir = tmp_path / "out"
    with pytest.raises(FileNotFoundError):
        common_helpers.get_checkpoint_path(checkpoint=out_dir)


def test_get_checkpoint_path__non_file(tmp_path: Path) -> None:
    out_dir = tmp_path / "out"
    out_dir.mkdir()
    with pytest.raises(ValueError):
        common_helpers.get_checkpoint_path(checkpoint=out_dir)


def test_get_out_path__nonexisting(tmp_path: Path) -> None:
    out_dir = tmp_path / "out"
    assert common_helpers.get_out_path(out=out_dir, overwrite=False) == out_dir


def test_get_out_path__existing__no_overwrite(tmp_path: Path) -> None:
    out_file = tmp_path / "file.txt"
    out_file.touch()
    with pytest.raises(ValueError):
        common_helpers.get_out_path(out=out_file, overwrite=False)


def test_get_out_path__existing_file__overwrite(tmp_path: Path) -> None:
    out_file = tmp_path / "file.txt"
    out_file.touch()
    assert common_helpers.get_out_path(out=out_file, overwrite=True) == out_file


def test_get_out_path__existing_dir__overwrite(tmp_path: Path) -> None:
    out_dir = tmp_path / "dir"
    out_dir.mkdir()
    with pytest.raises(ValueError):
        common_helpers.get_out_path(out=out_dir, overwrite=True)


def test_get_accelerator__set() -> None:
    """Test that same accelerator is returned if it is set."""
    assert common_helpers.get_accelerator(accelerator="cpu") == "cpu"
    accelerator = CPUAccelerator()
    assert common_helpers.get_accelerator(accelerator=accelerator) == accelerator


def test_get_out_dir(tmp_path: Path) -> None:
    assert (
        common_helpers.get_out_dir(out=tmp_path, resume=False, overwrite=False)
        == tmp_path
    )


def test_get_out_dir_nonexisting(tmp_path: Path) -> None:
    out_dir = tmp_path / "nonexisting"
    assert (
        common_helpers.get_out_dir(out=out_dir, resume=False, overwrite=False)
        == out_dir
    )


def test_get_out_dir__nondir(tmp_path: Path) -> None:
    out_dir = tmp_path / "file.txt"
    out_dir.touch()
    with pytest.raises(ValueError):
        common_helpers.get_out_dir(out=out_dir, resume=False, overwrite=False)


@pytest.mark.parametrize("resume", [True, False])
@pytest.mark.parametrize("overwrite", [True, False])
@pytest.mark.parametrize("rank_zero", [True, False])
def test_get_out_dir__nonempty(
    mocker: MockerFixture,
    tmp_path: Path,
    resume: bool,
    overwrite: bool,
    rank_zero: bool,
) -> None:
    (tmp_path / "some_file.txt").touch()
    mocker.patch.object(common_helpers, "is_rank_zero", return_value=rank_zero)
    if resume or overwrite or (not rank_zero):
        assert (
            common_helpers.get_out_dir(out=tmp_path, resume=resume, overwrite=overwrite)
            == tmp_path
        )
    else:
        with pytest.raises(ValueError):
            common_helpers.get_out_dir(out=tmp_path, resume=resume, overwrite=overwrite)


@pytest.mark.parametrize(
    "input_args, expected_output",
    [
        (
            {
                "model": Module(),
                "accelerator": CPUAccelerator(),
                "strategy": DDPStrategy(),
            },
            {
                "model": "Module",
                "accelerator": "CPUAccelerator",
                "strategy": "DDPStrategy",
            },
        ),
        (
            {"model": None, "accelerator": None, "strategy": None},
            {"model": None, "accelerator": None, "strategy": None},
        ),
        (
            {"model": Module(), "accelerator": None, "strategy": DDPStrategy()},
            {"model": "Module", "accelerator": None, "strategy": "DDPStrategy"},
        ),
    ],
)
def test_sanitize_config_dict(
    input_args: dict[str, Any], expected_output: dict[str, Any]
) -> None:
    assert common_helpers.sanitize_config_dict(input_args) == expected_output


def test_pretty_format_args() -> None:
    args = {
        "model_args": None,
        "num_nodes": 1,
        "num_workers": 8,
        "optim_args": {"lr": 0.0001},
        "out": "my_output_dir",
        "overwrite": False,
        "precision": "16-mixed",
        "resume": False,
        "seed": 0,
        "strategy": "auto",
        "trainer_args": None,
        "callbacks": None,
        "transform_args": None,
        "accelerator": "auto",
        "batch_size": 128,
        "data": "my_data_dir",
        "devices": "auto",
        "embed_dim": None,
        "epochs": 100,
        "loader_args": None,
        "method": "simclr",
        "method_args": {"temperature": 0.1},
        "model": "torchvision/resnet18",
    }
    # Assert that the args are ordered alphabetically.
    assert common_helpers.pretty_format_args(args=args) == (
        "{ 'accelerator': 'auto',\n"
        "  'batch_size': 128,\n"
        "  'callbacks': None,\n"
        "  'data': 'my_data_dir',\n"
        "  'devices': 'auto',\n"
        "  'embed_dim': None,\n"
        "  'epochs': 100,\n"
        "  'loader_args': None,\n"
        "  'method': 'simclr',\n"
        "  'method_args': {'temperature': 0.1},\n"
        "  'model': 'torchvision/resnet18',\n"
        "  'model_args': None,\n"
        "  'num_nodes': 1,\n"
        "  'num_workers': 8,\n"
        "  'optim_args': {'lr': 0.0001},\n"
        "  'out': 'my_output_dir',\n"
        "  'overwrite': False,\n"
        "  'precision': '16-mixed',\n"
        "  'resume': False,\n"
        "  'seed': 0,\n"
        "  'strategy': 'auto',\n"
        "  'trainer_args': None,\n"
        "  'transform_args': None}"
    )


def test_pretty_format_args__custom_model() -> None:
    assert (
        common_helpers.pretty_format_args(
            args={
                "model": models.resnet18(),
                "batch_size": 128,
                "epochs": 100,
            }
        )
        == "{'batch_size': 128, 'epochs': 100, 'model': 'ResNet'}"
    )

    class MyModel(Module):
        pass

    assert (
        common_helpers.pretty_format_args(
            args={
                "model": MyModel(),
                "batch_size": 128,
                "epochs": 100,
            }
        )
        == "{'batch_size': 128, 'epochs': 100, 'model': 'MyModel'}"
    )


@pytest.mark.parametrize(
    "num_workers,os_cpu_count,num_devices_per_node,expected_result",
    [
        (0, None, 1, 0),
        (8, None, 1, 8),
        (8, None, 3, 8),
        (64, None, 1, 64),
        (8, 64, 1, 8),
        ("auto", None, 1, 8),
        ("auto", 4, 1, 3),
        ("auto", 4, 2, 1),
        ("auto", 4, 3, 0),
        ("auto", 4, 4, 0),
        ("auto", 4, 8, 0),
        ("auto", 8, 1, 7),
        ("auto", 8, 3, 1),
        ("auto", 16, 1, 15),
        ("auto", 64, 7, 8),
    ],
)
def test_get_num_workers(
    mocker: MockerFixture,
    num_workers: int | Literal["auto"],
    os_cpu_count: int | None,
    num_devices_per_node: int,
    expected_result: int,
) -> None:
    mocker.patch.object(common_helpers.os, "cpu_count", return_value=os_cpu_count)
    assert (
        common_helpers.get_num_workers(
            num_workers=num_workers, num_devices_per_node=num_devices_per_node
        )
        == expected_result
    )


@pytest.mark.parametrize(
    "num_workers,num_devices_per_node,slurm_cpus_per_task,expected_result",
    [
        (0, 1, "8", 0),
        (1, 1, "8", 1),
        ("auto", 1, "8", 7),
        ("auto", 2, "8", 7),  # num_devices_per_node is ignored
        ("auto", 1, "", 8),  # fallback to default value of 8 workers
    ],
)
def test_get_num_workers__slurm(
    num_workers: int | Literal["auto"],
    num_devices_per_node: int,
    slurm_cpus_per_task: str,
    expected_result: int,
    mocker: MockerFixture,
) -> None:
    mocker.patch.dict(
        os.environ, {"SLURM_JOB_ID": "123", "SLURM_CPUS_PER_TASK": slurm_cpus_per_task}
    )
    assert (
        common_helpers.get_num_workers(
            num_workers=num_workers, num_devices_per_node=num_devices_per_node
        )
        == expected_result
    )
