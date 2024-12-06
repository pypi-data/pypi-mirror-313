# LightlyTrain

*Train models with self-supervised learning in a single command*

## Why LightlyTrain

Lightly**Train** uses self-supervised learning (SSL) to train models on large datasets
without the need for labels. It provides simple Python, Command Line, and Docker
interfaces to train models with popular SSL methods such as SimCLR or DINO. The trained
models are ideal starting points for fine-tuning on downstream tasks such as image
classification, object detection, and segmentation or for generating image embeddings.
Models trained with Lightly**Train** result in improved performance, faster convergence, and
better generalization compared to models trained without SSL. Image embeddings created
with Lightly**Train** capture more relevant information than their supervised counterparts
and seamlessly extend to new classes due to the unsupervised nature of SSL.

Lightly is the expert in SSL for computer vision and developed Lightly**Train** to simplify
model training for any task and dataset.

## Features

- Train models on any image data without labels
- Train models from popular libraries such as [torchvision](https://github.com/pytorch/vision), [TIMM](https://github.com/huggingface/pytorch-image-models), [Ultralytics](https://github.com/ultralytics/ultralytics), and [SuperGradients](https://github.com/Deci-AI/super-gradients)
- Train custom models
- No SSL expertise required
- Automatic SSL method selection (soon!)
- Python, Command Line, and Docker support
- Multi-GPU and multi-node support
- Export models for fine-tuning or inference
- Generate and export image embeddings
- Monitor training progress with TensorBoard, Weights & Biases, Neptune, etc. (soon!)

## License

Lightly**Train** is available under an AGPL-3.0 and a commercial license. Please contact us
at info@lightly.ai for more information.

## Contact

- [**Email**](info@lightly.ai)
- [**Website**](https://www.lightly.ai/lightlytrain)
- [**Discord**](https://discord.gg/xvNJW94)
