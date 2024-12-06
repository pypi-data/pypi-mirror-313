(installation)=

# Installation

Lightly**Train** is available on [PyPI](https://pypi.org/project/lightly-train/) and can be installed via pip or other package managers.

```bash
pip install lightly-train
```

To update to the latest version, run:

```bash
pip install --upgrade lightly-train
```

See {ref}`docker` for Docker installation instructions.

(optional-dependencies)=

## Optional Dependencies

Lightly**Train** has optional dependencies that are not installed by default. The following dependencies are available:

### Logging

- `tensorboard`: For logging to [TensorBoard](#tensorboard)
- `wandb`: For logging to [Weights & Biases](#wandb)

### Model Support

- `super-gradients`: For [SuperGradients](#super-gradients) models
- `timm`: For [TIMM](#timm) models
- `ultralytics`: For [Ultralytics](#ultralytics) models

To install optional dependencies, run:

```bash
pip install lightly-train[tensorboard]
```

Or for multiple optional dependencies:

```bash
pip install lightly-train[tensorboard,timm]
```
