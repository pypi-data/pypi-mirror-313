(models)=

# Models

Lightly**Train** supports training models from various libraries. See [Supported Libraries](#supported-libraries)
for a list of supported libraries and models.

The model is specified in the `train` command with the `model` argument:

````{tab} Python
```python
import lightly_train

lightly_train.train(
    out="out/my_experiment",
    data="my_data_dir",
    model="torchvision/resnet50",
    method="dino",
)
````

````{tab} Command Line
```bash
lightly-train train out="out/my_experiment" data="my_data_dir" model="torchvision/resnet50" method="dino"
````

Model names always follow the pattern `<library name>/<model name>`.

Instead of passing a model name, it is also possible to pass a model instance directly
to the `train` function:

````{tab} Python
```python
import lightly_train
from torchvision.models import resnet50

model = resnet50()

lightly_train.train(
    out="out/my_experiment",
    data="my_data_dir",
    model=model,
    method="dino",
)
````

## List Models

The `list_models` command lists all available models. Only models from installed
packages are listed.

````{tab} Python
```python
import lightly_train

print(lightly_train.list_models())
````

````{tab} Command Line
```bash
lightly-train list_models
````

(models-supported-libraries)=

## Supported Libraries

The following libraries are supported:

- [Torchvision](#torchvision)
- [TIMM](#timm)
- [Ultralytics](#ultralytics)
- [SuperGradients](#supergradients)

(torchvision)=

### Torchvision

**Supported models**

- ResNet
  - `torchvision/resnet18`
  - `torchvision/resnet34`
  - `torchvision/resnet50`
  - `torchvision/resnet101`
  - `torchvision/resnet152`
- ConvNext
  - `torchvision/convnext_base`
  - `torchvision/convnext_large`
  - `torchvision/convnext_small`
  - `torchvision/convnext_tiny`

(timm)=

### TIMM

```{important}
[TIMM](https://github.com/huggingface/pytorch-image-models) must be installed with
`pip install lightly-train[timm]`.
```

**Supported models**

- `timm/<model name>` (all models are supported, see [timm docs](https://github.com/huggingface/pytorch-image-models?tab=readme-ov-file#models) for a full list)

Examples

- `timm/resnet50`
- `timm/convnext_base`
- `timm/vit_base_patch16_224`

(ultralytics)=

### Ultralytics

```{important}
[Ultralytics](https://github.com/ultralytics/ultralytics) must be installed with
`pip install lightly-train[ultralytics]`.
```

```{warning}
Using Ultralytics models might require a commercial Ultralytics license. See the
[Ultralytics website](https://www.ultralytics.com/license) for more information.
```

Models ending with `.pt` load pre-trained weights by Ultralytics. Models ending with
`.yaml` are not pre-trained.

**Supported models**

- YOLOv5
  - `ultralytics/yolov5l.yaml`
  - `ultralytics/yolov5l6u.pt`
  - `ultralytics/yolov5lu.pt`
  - `ultralytics/yolov5lu.yaml`
  - `ultralytics/yolov5m.yaml`
  - `ultralytics/yolov5m6u.pt`
  - `ultralytics/yolov5mu.pt`
  - `ultralytics/yolov5mu.yaml`
  - `ultralytics/yolov5n.yaml`
  - `ultralytics/yolov5n6u.pt`
  - `ultralytics/yolov5nu.pt`
  - `ultralytics/yolov5nu.yaml`
  - `ultralytics/yolov5s.yaml`
  - `ultralytics/yolov5s6u.pt`
  - `ultralytics/yolov5su.pt`
  - `ultralytics/yolov5su.yaml`
  - `ultralytics/yolov5x.yaml`
  - `ultralytics/yolov5x6u.pt`
  - `ultralytics/yolov5xu.pt`
  - `ultralytics/yolov5xu.yaml`
- YOLOv6
  - `ultralytics/yolov6l.yaml`
  - `ultralytics/yolov6m.yaml`
  - `ultralytics/yolov6n.yaml`
  - `ultralytics/yolov6s.yaml`
  - `ultralytics/yolov6x.yaml`
- YOLOv8
  - `ultralytics/yolov8l-cls.pt`
  - `ultralytics/yolov8l-cls.yaml`
  - `ultralytics/yolov8l-obb.pt`
  - `ultralytics/yolov8l-obb.yaml`
  - `ultralytics/yolov8l-oiv7.pt`
  - `ultralytics/yolov8l-pose.pt`
  - `ultralytics/yolov8l-pose.yaml`
  - `ultralytics/yolov8l-seg.pt`
  - `ultralytics/yolov8l-seg.yaml`
  - `ultralytics/yolov8l-world.pt`
  - `ultralytics/yolov8l-world.yaml`
  - `ultralytics/yolov8l-worldv2.pt`
  - `ultralytics/yolov8l-worldv2.yaml`
  - `ultralytics/yolov8l.pt`
  - `ultralytics/yolov8l.yaml`
  - `ultralytics/yolov8m-cls.pt`
  - `ultralytics/yolov8m-cls.yaml`
  - `ultralytics/yolov8m-obb.pt`
  - `ultralytics/yolov8m-obb.yaml`
  - `ultralytics/yolov8m-oiv7.pt`
  - `ultralytics/yolov8m-pose.pt`
  - `ultralytics/yolov8m-pose.yaml`
  - `ultralytics/yolov8m-seg.pt`
  - `ultralytics/yolov8m-seg.yaml`
  - `ultralytics/yolov8m-world.pt`
  - `ultralytics/yolov8m-world.yaml`
  - `ultralytics/yolov8m-worldv2.pt`
  - `ultralytics/yolov8m-worldv2.yaml`
  - `ultralytics/yolov8m.pt`
  - `ultralytics/yolov8m.yaml`
  - `ultralytics/yolov8n-cls.pt`
  - `ultralytics/yolov8n-cls.yaml`
  - `ultralytics/yolov8n-obb.pt`
  - `ultralytics/yolov8n-obb.yaml`
  - `ultralytics/yolov8n-oiv7.pt`
  - `ultralytics/yolov8n-pose.pt`
  - `ultralytics/yolov8n-pose.yaml`
  - `ultralytics/yolov8n-seg.pt`
  - `ultralytics/yolov8n-seg.yaml`
  - `ultralytics/yolov8n.pt`
  - `ultralytics/yolov8n.yaml`
  - `ultralytics/yolov8s-cls.pt`
  - `ultralytics/yolov8s-cls.yaml`
  - `ultralytics/yolov8s-obb.pt`
  - `ultralytics/yolov8s-obb.yaml`
  - `ultralytics/yolov8s-oiv7.pt`
  - `ultralytics/yolov8s-pose.pt`
  - `ultralytics/yolov8s-pose.yaml`
  - `ultralytics/yolov8s-seg.pt`
  - `ultralytics/yolov8s-seg.yaml`
  - `ultralytics/yolov8s-world.pt`
  - `ultralytics/yolov8s-world.yaml`
  - `ultralytics/yolov8s-worldv2.pt`
  - `ultralytics/yolov8s-worldv2.yaml`
  - `ultralytics/yolov8s.pt`
  - `ultralytics/yolov8s.yaml`
  - `ultralytics/yolov8x-cls.pt`
  - `ultralytics/yolov8x-cls.yaml`
  - `ultralytics/yolov8x-obb.pt`
  - `ultralytics/yolov8x-obb.yaml`
  - `ultralytics/yolov8x-oiv7.pt`
  - `ultralytics/yolov8x-pose.pt`
  - `ultralytics/yolov8x-pose.yaml`
  - `ultralytics/yolov8x-seg.pt`
  - `ultralytics/yolov8x-seg.yaml`
  - `ultralytics/yolov8x-world.pt`
  - `ultralytics/yolov8x-world.yaml`
  - `ultralytics/yolov8x-worldv2.pt`
  - `ultralytics/yolov8x-worldv2.yaml`
  - `ultralytics/yolov8x.pt`
  - `ultralytics/yolov8x.yaml`

(super-gradients)=

### SuperGradients

```{important}
[SuperGradients](https://github.com/Deci-AI/super-gradients) must be installed with
`pip install lightly-train[super-gradients]`.
```

```{warning}
SuperGradients support is still experimental. There might be unexpected warnings in
the logs.
```

**Supported models**

- PP-LiteSeg
  - `super_gradients/pp_lite_b_seg`
  - `super_gradients/pp_lite_b_seg50`
  - `super_gradients/pp_lite_b_seg75`
  - `super_gradients/pp_lite_t_seg`
  - `super_gradients/pp_lite_t_seg50`
  - `super_gradients/pp_lite_t_seg75`
- SSD
  - `super_gradients/ssd_lite_mobilenet_v2`
  - `super_gradients/ssd_mobilenet_v1`
- YOLO-NAS
  - `super_gradients/yolo_nas_l`
  - `super_gradients/yolo_nas_m`
  - `super_gradients/yolo_nas_pose_l`
  - `super_gradients/yolo_nas_pose_m`
  - `super_gradients/yolo_nas_pose_n`
  - `super_gradients/yolo_nas_pose_s`
  - `super_gradients/yolo_nas_s`

```{toctree}
---
hidden:
maxdepth: 1
---
custom_models
```

% Alternative reference to avoid overwriting the reference to the custom models page.
(models-custom-models)=

## Custom Models

See {ref}`Custom Models <custom-models>` for information on how to train custom models.
