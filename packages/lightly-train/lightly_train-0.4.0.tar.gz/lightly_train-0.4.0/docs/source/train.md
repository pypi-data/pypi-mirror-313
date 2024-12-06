(train)=

# Train

The train command is a simple interface to pretrain a large number of models using
different SSL methods. An example command looks like this:

````{tab} Python
```python
import lightly_train

lightly_train.train(
    out="out/my_experiment",
    data="my_data_dir",
    model="torchvision/resnet50",
    method="dino",
    epochs=100,
    batch_size=128,
)
````

````{tab} Command Line
```bash
lightly-train train out="out/my_experiment" data="my_data_dir" model="torchvision/resnet50" method="dino" epochs=100 batch_size=128
````

This will pretrain a ResNet-50 model from TorchVision using images from `my_data_dir`
and the DINO self-supervised learning method. All training logs and checkpoints
are saved to the output directory at `out/my_experiment`.

```{tip}
See {meth}`lightly_train.train` for a complete list of available arguments.
```

(train-output)=

## Out

The `out` argument specifies the output directory where all training logs and
checkpoints are saved. It looks like this after training:

```text
out/my_experiment
├── checkpoints
│   ├── epoch=99-step=123.ckpt                          # Intermediate checkpoint
│   └── last.ckpt                                       # Last checkpoint
├── events.out.tfevents.1721899772.host.1839736.0       # TensorBoard logs
├── metrics.jsonl                                       # Training metrics
└── train.log                                           # Training logs
```

The final model checkpoint is saved to `out/my_experiment/checkpoints/last.ckpt`.

```{tip}
Create a new output directory for each experiment to keep training logs and
checkpoints organized.
```

(train-data)=

## Data

The data directory `data="my_data_dir"` can have any structure, including nested
subdirectories. Lightly**Train** finds all images in the directory recursively.

The following image formats are supported:

- jpg
- jpeg
- png
- ppm
- bmp
- pgm
- tif
- tiff
- webp

## Model

See [](#models) for a list of all supported models.

## Method

See [](#methods) for a list of all supported methods.

(logging)=

## Loggers

Logging is configured with the `loggers` argument. The following loggers are
supported:

- [`jsonl`](#jsonl): Logs training metrics to a .jsonl file (enabled by default)
- [`tensorboard`](#tensorboard): Logs training metrics to TensorBoard (enabled by
  default, requires TensorBoard to be installed)
- [`wandb`](#wandb): Logs training metrics to Weights & Biases (disabled by
  default, requires Weights & Biases to be installed)

(jsonl)=

### JSONL

The JSONL logger is enabled by default and logs training metrics to a .jsonl file
at `out/my_experiment/metrics.jsonl`.

Disable the JSONL logger with:

````{tab} Python
```python
loggers={"jsonl": None}
````

````{tab} Command Line
```bash
loggers.jsonl=null
````

(tensorboard)=

### TensorBoard

```{important}
TensorBoard must be installed with `pip install lightly-train[tensorboard]`.
```

TensorBoard logs are automatically saved to the output directory. Run TensorBoard in
a new terminal to visualize the training progress:

```bash
tensorboard --logdir out/my_experiment
```

Disable the TensorBoard logger with:

````{tab} Python
```python
loggers={"tensorboard": None}
````

````{tab} Command Line
```bash
loggers.tensorboard=null
````

(wandb)=

### Weights & Biases

```{important}
Weights & Biases must be installed with `pip install lightly-train[wandb]`.
```

The Weights & Biases logger can be configured with the following arguments:

````{tab} Python
```python
import lightly_train

lightly_train.train(
    out="out/my_experiment",
    data="my_data_dir",
    model="torchvision/resnet50",
    method="dino",
    loggers={
        "wandb": {
            "project": "my_project",
            "name": "my_experiment",
            "log_model": False,              # Set to True to upload model checkpoints
        },
    },
)
````

````{tab} Command Line
```bash
lightly-train train out="out/my_experiment" data="my_data_dir" model="torchvision/resnet50" method="dino" loggers.wandb.project="my_project" loggers.wandb.name="my_experiment" loggers.wandb.log_model=False
````

More configuration options are available through the Weights & Biases environment
variables. See the [Weights & Biases documentation](https://docs.wandb.ai/guides/track/environment-variables/)
for more information.

Disable the Weights & Biases logger with:

````{tab} Python
```python
loggers={"wandb": None}
````

````{tab} Command Line
```bash
loggers.wandb=null
````

## Advanced Options

### Input Image Resolution

The input image resolution can be set with the transform_args argument. By default a
resolution of 224x224 pixels is used. A custom resolution can be set like this:

````{tab} Python
```python
transform_args = {"image_size": (448, 448)} # (height, width)
````

````{tab} Command Line
```bash
transform_args.image_size="\[448,448\]"  # (height, width)
````

```{warning}
Not all models support all image sizes.
```

### Performance Optimizations

For performance optimizations, e.g. using accelerators, multi-GPU, multi-node, and half precision training, see the [performance](#performance) page.
