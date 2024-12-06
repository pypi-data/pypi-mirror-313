# ![LightlyTrain -  Build better computer vision models faster with self-supervised pre-training](./_static/lightly_train.svg)

*Build better computer vision models faster with self-supervised pre-training*

## Why LightlyTrain?

Lightly**Train** uses self-supervised learning (SSL) to train computer vision models on
large datasets **without labels**. It provides simple Python, Command Line, and Docker
interfaces to train models with popular SSL methods such as DINO and SimCLR.

The trained models are ideal starting points for fine-tuning on downstream tasks such as
image **classification**, **object detection**, and **segmentation** or for generating
**image embeddings**. Models trained with Lightly**Train** result in
**improved performance**, **faster convergence**, and better **generalization** compared
to models trained without SSL. Image embeddings created with Lightly**Train** capture more
relevant information than their supervised counterparts and seamlessly extend to new
classes due to the unsupervised nature of SSL.

Lightly is the expert in SSL for computer vision and developed Lightly**Train** to simplify
model training for any task and dataset.

## How It Works

### Train a Model with SSL

```python
import lightly_train

ligthly_train.train(
    out="out/my_experiment",            # Output directory
    data="my_data_dir",                 # Directory with images
    model="torchvision/resnet50",       # Model to train
    method="dino",                      # Self-supervised learning method
)
```

After training is complete, you can either [export the model](#export-the-model-for-fine-tuning)
for fine-tuning or use the model to [generate image embeddings](#generate-image-embeddings).

### Export the Model for Fine-Tuning

```python
import lightly_train

lightly_train.export(
    out="my_exported_model.pth",                            # Exported model
    checkpoint="out/my_experiment/checkpoints/last.ckpt",   # LightlyTrain checkpoint
    part="model",                                           # Model part to export
    format="torch_state_dict",                              # Export format
)
```

You can now fine-tune the exported model with your favorite library.

### Generate Image Embeddings

```python
import lightly_train

lightly_train.embed(
    out="my_embeddings.pth",                                # Exported embeddings
    checkpoint="out/my_experiment/checkpoints/last.ckpt",   # LightlyTrain checkpoint
    data="my_data_dir",                                     # Directory with images
    format="torch",                                         # Embedding format
)
```

You can now use the generated embeddings for clustering, retrieval, or visualization
tasks.

The [quick start guide](#quick-start) shows in more detail how to install and use
Lightly**Train**.

## Features

- Train models on any image data without labels
- Train models from popular libraries such as [torchvision](https://github.com/pytorch/vision), [TIMM](https://github.com/huggingface/pytorch-image-models), [Ultralytics](https://github.com/ultralytics/ultralytics), and [SuperGradients](https://github.com/Deci-AI/super-gradients)
- Train [custom models](#custom-models) with ease
- No self-supervised learning expertise required
- Automatic SSL method selection (coming soon!)
- Python, Command Line, and Docker support
- Built for [high performance](#performance) including [Multi-GPU](#multi-gpu) and [multi-node](#multi-node) support
- {ref}`Export models <export>` for fine-tuning or inference
- Generate and export {ref}`image embeddings <embed>`
- [Monitor training progress](#logging) with TensorBoard, Weights & Biases, and more

### Supported Models

[**Torchvision**](#torchvision)

- ResNet
- ConvNext

[**TIMM**](#timm)

- All models

[**Ultralytics**](#ultralytics)

- YOLOv5
- YOLOv6
- YOLOv8

[**SuperGradients**](#super-gradients)

- PP-LiteSeg
- SSD
- YOLO-NAS

See [supported models](#models-supported-libraries) for a detailed list of all supported
models.

[Contact](#contact) us if you need support for additional models or libraries.

### Supported SSL Methods

- DINO
- DenseCL (experimental)
- SimCLR

See [methods](#methods) for details.

```{toctree}
---
hidden:
maxdepth: 2
---
quick_start
installation
train
export
embed
models/index
methods/index
performance/index
docker
python_api/index
changelog
```

## License

Lightly**Train** is available under an AGPL-3.0 and a commercial license. Please contact us
at [info@lightly.ai](mailto:info@lightly.ai) for more information.

## Contact

[**Email**](mailto:info@lightly.ai) | [**Website**](https://www.lightly.ai/lightlytrain) | [**Discord**](https://discord.gg/xvNJW94)
