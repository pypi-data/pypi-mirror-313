(export)=

# Export

The `export` command is used to prepare a model for fine-tuning or inference. It allows
exporting the model from [training checkpoints](#train-output) which contain additional
information such as optimizer states that are not needed for fine-tuning or inference.

````{tab} Python
```python
import lightly_train

lightly_train.train(
    out="out/my_experiment",
    data="my_data_dir",
    model="torchvision/resnet50",
    method="dino",
)

lightly_train.export(
    out="my_exported_model.pth",
    checkpoint="out/my_experiment/checkpoints/last.ckpt",
    part="model",
    format="torch_state_dict",
)
````

````{tab} Command Line
```bash
lightly-train train out="out/my_experiment" data="my_data_dir" model="torchvision/resnet50" method="dino"
lightly-train export out="my_exported_model.pth" checkpoint="out/my_experiment/checkpoints/last.ckpt" part="model" format="torch_state_dict"
````

The above code example trains a model and exports the last training checkpoint as a
torch state dictionary.

```{tip}
See {meth}`lightly_train.export` for a complete list of arguments.
```

```{warning}
It is recommended to always export the model after training as the training checkpoints
include not only the model weights but also the model code. If modifications are made to
the codebase after training, the Lightly**Train** checkpoint might not be loadable anymore
in the future. Exporting the model as a torch state dict ensures that the model can be
loaded in the future even if the codebase changes.
```

## Out

The `out` argument specifies the output file where the exported model is saved.

## Checkpoint

The `checkpoint` argument specifies the Lightly**Train** checkpoint to use for exporting the
model. This is the checkpoint saved to `out/my_experiment/checkpoints/last.ckpt` after
training.

(export-format)=

## Format

The `format` argument specifies the format in which the model is exported. The following
formats are supported.

- `torch_state_dict` (Recommended)

  Only the model's state dict is saved which can be loaded with:

  ```python
  from torchvision.models import resnet50

  model = resnet50()
  model.load_state_dict(torch.load("my_exported_model.pth"))
  ```

  This is the recommended format and ensures compatibility with different Lightly**Train**
  versions.

- `torch_model`

  The model is saved as a torch module which can be loaded with:

  ```python
  import torch

  model = torch.load("my_exported_model.pth")
  ```

  This requires that the same Lightly**Train** version is installed when the model is
  exported and when it is loaded again.

  - `ultralytics`

    The model is saved as an ultralytics model which can be loaded with:

    ```python
    from ultralytics import YOLO

    model = YOLO("my_exported_model.pth")
    ```

(export-part)=

## Part

The `part` argument specifies which part of the model to export. The following parts are
supported.

- `model`

  Exports the model as passed with the `model` argument in the `train` function.

- `embedding_model`

  Exports the embedding model. This includes the model passed with the `model` argument
  in the `train` function and an extra embedding layer if the `embed_dim` argument was
  set during training. This is useful if you want to use the model for embedding images.
