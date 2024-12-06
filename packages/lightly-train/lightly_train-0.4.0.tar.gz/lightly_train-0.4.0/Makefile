### Cleaning

.PHONY: clean
clean: clean-build clean-pyc clean-out

# remove build artifacts
.PHONY: clean-build
clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -fr {} +

# remove python file artifacts
.PHONY: clean-pyc
clean-pyc:
	find . -name '__pycache__' -exec rm -fr {} +

# remove hydra outputs
.PHONY: clean-out
clean-out:
	rm -fr outputs/
	rm -fr lightly_outputs/
	rm -fr lightning_logs/
	rm -fr lightly_epoch_*.ckpt
	rm -fr last.ckpt

### Formatting and type-checking

# run format and type checks and tests
.PHONY: all-checks
all-checks: static-checks test

# run format and type checks
.PHONY: static-checks
static-checks: format-check type-check

# Files to format with mdformat.
# This is needed to avoid formatting files in .venv. The mdformat command has an
# --exclude option but only on Python 3.13+.
MDFORMAT_FILES := .github docker docs src tests *.md

# run formatter
.PHONY: format
format: add-header
	# Format code
	ruff format .
	# Fix linting issues and sort imports
	ruff check --fix .
	# Format markdown files
	mdformat ${MDFORMAT_FILES}

# run format check
.PHONY: format-check
format-check:
	# Check code formatting
	ruff check .
	# Check markdown formatting
	mdformat --check ${MDFORMAT_FILES}

# run type check
.PHONY: type-check
type-check:
	mypy src tests

# adding the license header to all files
.PHONY: add-header
add-header:
	licenseheaders -t dev_tools/licenseheader.tmpl -d src
	licenseheaders -t dev_tools/licenseheader.tmpl -d tests



### Testing

# run tests
.PHONY: test
test:
	pytest tests

.PHONY: test-ci
test-ci:
	pytest tests -v


### Virtual Environment

.PHONY: install-uv
install-uv:
	curl -LsSf https://astral.sh/uv/0.5.4/install.sh | sh


.PHONY: reset-venv
reset-venv:
	deactivate || true
	rm -rf .venv
	uv venv .venv


### Dependencies

# When running these commands locally, it is recommended to first reset the environment
# with: `make reset-venv && source .venv/bin/activate`
# Otherwise old dependencies might linger around.

# Set EDITABLE to -e to install the package in editable mode outside of CI. This is
# useful for local development.
ifdef CI
EDITABLE :=
else
EDITABLE := -e
endif

# SuperGradients is not compatible with Python>=3.10. It is also not easy to install
# on MacOS. Therefore we exclude it from the default extras.
EXTRAS := [dev,tensorboard,timm,ultralytics,wandb]
# Exclude ultralytics from docker extras as it has an AGPL license and we should not
# distribute it with the docker image.
DOCKER_EXTRAS := --extra tensorboard --extra timm --extra wandb

# Date until which dependencies installed with --exclude-newer must have been released.
# Dependencies released after this date are ignored.
EXCLUDE_NEWER_DATE := "2024-11-15"
# Pinned versions for Torch and TorchVision to avoid issues with the CUDA version on the CI machine.
# These versions are compatible with CUDA 11.4 and Python 3.8. They are the latest versions
# available before 2024-08-28.
PINNED_TORCH_VERSION := "2.4.0+cu118"
PINNED_TORCHVISION_VERSION := "0.19.0+cu118"

# Install ffmpeg on Ubuntu.
. PHONY: install-ffmpeg-ubuntu
install-ffmpeg-ubuntu:
	sudo apt-get install ffmpeg=7:4.2.7-0ubuntu0.1

# Install package for local development.
.PHONY: install-dev
install-dev:
	uv pip install ${EDITABLE} ".${EXTRAS}"

# Install package with minimal dependencies.
#
# This command is split into multiple steps:
# 1. Install the dev dependencies to be able to run tests. We don't want to use
#    the minimal versions for these dependencies.
# 2. Then we reinstall the package with minimal dependencies.
#
# Explanation of flags:
# --exclude-newer: We don't want to install dependencies released after that date to
#   keep CI stable.
# --resolution=lowest-direct: Only install minimal versions for direct dependencies.
#   Transitive dependencies will use the latest compatible version.
# 	Using --resolution=lowest would also download the latest versions for transitive
#   dependencies which is not a realistic scenario and results in some extremely old
#   dependencies being installed.
# --reinstall: Reinstall dependencies to make sure they satisfy the constraints.
.PHONY: install-minimal
install-minimal:
	uv pip install --exclude-newer ${EXCLUDE_NEWER_DATE} ${EDITABLE} ".[dev]"
	uv pip install --resolution=lowest-direct --exclude-newer ${EXCLUDE_NEWER_DATE} --reinstall ${EDITABLE} "."

# Install package with minimal dependencies including extras.
# See install-minimal for more information.
.PHONY: install-minimal-extras
install-minimal-extras:
	uv pip install --exclude-newer ${EXCLUDE_NEWER_DATE} ${EDITABLE} ".[dev]"
	uv pip install --resolution=lowest-direct --exclude-newer ${EXCLUDE_NEWER_DATE} --reinstall ${EDITABLE} ".${EXTRAS}"

# Install package for Python 3.8 with dependencies pinned to the latest compatible
# version available at EXCLUDE_NEWER_DATE. This keeps CI stable if new versions of
# dependencies are released.
#
# We have to differentiate between Python versions because SuperGradients is not
# compatible with Python>=3.10. For 3.8 we install the package with all extras,
# including SuperGradients.
#
# Torch and TorchVision are pinned to specific versions to avoid issues with the
# CUDA version on the CI machine. See PINNED_TORCH_VERSION and PINNED_TORCHVISION_VERSION
# for the pinned versions.
.PHONY: install-pinned-3.8
install-pinned-3.8:
	uv pip install --exclude-newer ${EXCLUDE_NEWER_DATE} --reinstall ${EDITABLE} . --all-extras --requirement pyproject.toml
	uv pip install \
		"torch==${PINNED_TORCH_VERSION}" "torchvision==${PINNED_TORCHVISION_VERSION}" \
		--index-url https://download.pytorch.org/whl/cu118 --reinstall

# Install package for Python 3.11 with dependencies pinned to the latest compatible
# version available at EXCLUDE_NEWER_DATE.
#
# See install-pinned-3.8 for more information.
.PHONY: install-pinned-3.11
install-pinned-3.11:
	uv pip install --exclude-newer ${EXCLUDE_NEWER_DATE} --reinstall ${EDITABLE} ".${EXTRAS}"
	uv pip install \
		"torch==${PINNED_TORCH_VERSION}" "torchvision==${PINNED_TORCHVISION_VERSION}" \
		--index-url https://download.pytorch.org/whl/cu118 --reinstall

# Install package with the latest dependencies.
.PHONY: install-latest
install-latest:
	uv pip install --upgrade --reinstall ${EDITABLE} ".${EXTRAS}"

# Install package dependencies in Docker image.
.PHONY: install-docker-dependencies
install-docker-dependencies:
	uv pip install -v --exclude-newer ${EXCLUDE_NEWER_DATE} ${DOCKER_EXTRAS} --requirement pyproject.toml
	uv pip uninstall pillow
	C="cc -mavx2" uv pip install --exclude-newer ${EXCLUDE_NEWER_DATE} --upgrade --force-reinstall pillow-simd

# Install package in Docker image.
# This requires `install-docker-dependencies` to be run first. We don't add this command
# as a dependency to not run it multiple times accidentally.
.PHONY: install-docker
install-docker:
	uv pip install -v --no-deps .

# Install dependencies for building and publishing the package.
.PHONY: install-dist
install-dist:
	uv pip install --exclude-newer ${EXCLUDE_NEWER_DATE} wheel twine build 

### Building source and wheel package for publishing to pypi
.PHONY: dist
dist: clean
	python -m build
	ls -l dist
