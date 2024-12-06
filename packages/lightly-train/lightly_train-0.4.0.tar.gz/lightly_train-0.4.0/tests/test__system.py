#
# Copyright (c) Lightly AG and affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
import logging

from pytest import LogCaptureFixture
from pytest_mock import MockerFixture

import lightly_train
from lightly_train import _system
from lightly_train._system import DependencyInformation, SystemInformation


def test_get_system_information() -> None:
    # NOTE(Philipp, 11/24): This simply tests that the (function does not fail.
    system_information = _system.get_system_information()
    assert lightly_train.__version__ == system_information.lightly_train_version


def test_log_system_information(
    mocker: MockerFixture, caplog: LogCaptureFixture
) -> None:
    gpu_device_properties = mocker.MagicMock()
    gpu_device_properties.name = "Mock GPU"
    gpu_device_properties.total_memory = 1024
    gpu_device_properties.major = 7
    gpu_device_properties.minor = 5

    system_information = SystemInformation(
        platform="Linux-5.15.0-1031-aws-x86_64-with-glibc2.31",
        python_version="3.10.6",
        lightly_train_version="0.3.2",
        dependencies=[DependencyInformation(library="my_dependency", version="0.1.0")],
        optional_dependencies=[
            DependencyInformation(library="my_optional", version="0.2.0"),
            DependencyInformation(library="my_non_installed", version=None),
        ],
        cpu_count=8,
        gpus=[gpu_device_properties],
    )

    with caplog.at_level(logging.DEBUG):
        _system.log_system_information(system_information=system_information)
        assert "Platform: Linux-5.15.0-1031-aws-x86_64-with-glibc2.31" in caplog.text
        assert "Python: 3.10.6" in caplog.text
        assert "LightlyTrain: 0.3.2" in caplog.text
        # Dependencies
        assert " - my_dependency               0.1.0" in caplog.text
        # Optional dependencies
        assert " - my_optional                 0.2.0" in caplog.text
        assert " - my_non_installed                x" in caplog.text
        # CPUs and GPUs
        assert "CPUs: 8" in caplog.text
        assert " - Mock GPU 7.5 (1024)"
