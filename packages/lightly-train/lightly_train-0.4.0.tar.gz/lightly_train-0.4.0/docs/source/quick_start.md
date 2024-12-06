(quick-start)=

# Quick Start

## Installation

```bash
pip install lightly-train[tensorboard]
```

## Prepare Data

You can use any image dataset for training. No labels are required, and the dataset can
be structured in any way, including subdirectories. If you don't have a dataset at hand,
you can download one like this:

```bash
git clone https://github.com/lightly-ai/dataset_clothing_images.git my_data_dir
```

See the [data guide](#train-data) for more information on supported data formats.

## Train

Once the data is ready, you can train the model like this:

````{tab} Python
```python
import lightly_train

lightly_train.train(
    out="out/my_experiment",            # Output directory
    data="my_data_dir",                 # Directory with images
    model="torchvision/resnet18",       # Model to train
    method="dino",                      # Self-supervised learning method
    epochs=100,                         # Number of epochs to train
    batch_size=128,                     # Batch size
)
````

````{tab} Command Line
```bash
lightly-train train out="out/my_experiment" data="my_data_dir" model="torchvision/resnet18" method="dino" epochs=100 batch_size=128
````

```{tip}
Decrease the number of epochs and batch size for faster training.
```

This will pretrain a Torchvision ResNet-18 model using images from `my_data_dir` and the
DINO self-supervised learning method. All training logs and checkpoints are saved to the
output directory at `out/my_experiment`.

Once the training is complete, the `out/my_experiment` directory should contain the
following files:

```text
out/my_experiment
├── checkpoints
│   ├── epoch=99-step=123.ckpt          # Intermediate checkpoint
│   └── last.ckpt                       # Last checkpoint
├── events.out.tfevents.123.0           # Tensorboard logs
├── metrics.jsonl                       # Training metrics
└── train.log                           # Training logs
```

The most important file is `out/my_experiment/checkpoints/last.ckpt`, which contains the
final model checkpoint.

While the trained model has already learned good representations of the images, it
cannot yet make any predictions for tasks such as classification, detection, or
segmentation. To solve these tasks, the model needs to be fine-tuned on a labeled
dataset.

## Export

Before the model can be fine-tuned, it needs to be exported. The `export` command makes
sure that only the model weights needed for fine-tuning are exported from the
Lightly**Train** checkpoint:

````{tab} Python
```python
import lightly_train

lightly_train.export(
    out="my_exported_model.pth",                            # Exported model
    checkpoint="out/my_experiment/checkpoints/last.ckpt",   # LightlyTrain checkpoint
    part="model",                                           # Export ResNet-18 model with classification head
    format="torch_state_dict",                              # Export format
)
````

````{tab} Command Line
```bash
lightly-train export out="my_exported_model.pth" checkpoint="out/my_experiment/checkpoints/last.ckpt" part="model" format="torch_state_dict"
````

## Fine-Tune

Now the model is ready for fine-tuning! You can use your favorite library for this step.
Below is a simple example using PyTorch:

```python
import torch
from torch import nn, optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms, models

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])
dataset = datasets.ImageFolder(root="my_data_dir", transform=transform)
dataloader = DataLoader(dataset, batch_size=16, shuffle=True, drop_last=True)

# Load the exported model
model = models.resnet18()
model.load_state_dict(torch.load("my_exported_model.pth", weights_only=True))

# Update the classification head with the correct number of classes
model.fc = nn.Linear(model.fc.in_features, len(dataset.classes))

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

print("Starting fine-tuning...")
num_epochs = 10
for epoch in range(num_epochs):
    for inputs, labels in dataloader:
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
    print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}")
```

The output should show the loss decreasing over time:

```text
Starting fine-tuning...
Epoch [1/10], Loss: 2.1686
Epoch [2/10], Loss: 2.1290
Epoch [3/10], Loss: 2.1854
Epoch [4/10], Loss: 2.2936
Epoch [5/10], Loss: 1.9303
Epoch [6/10], Loss: 1.9949
Epoch [7/10], Loss: 1.8429
Epoch [8/10], Loss: 1.9873
Epoch [9/10], Loss: 1.8179
Epoch [10/10], Loss: 1.5360
```

Congratulations! You just trained and fine-tuned a model using Lightly**Train**!

```{tip}
Lightly**Train** has integrated support for popular libraries such as [Ultralytics](#ultralytics)
and [SuperGradients](#super-gradients), which allow you to fine-tune the exported models
directly from the command line.
```

## Embed

Instead of fine-tuning the model, you can also use it to generate image embeddings. This
is useful for clustering, retrieval, or visualization tasks. The `embed` command
generates embeddings for all images in a directory:

````{tab} Python
```python
import lightly_train

lightly_train.embed(
    out="my_embeddings.pth",                                # Exported embeddings
    checkpoint="out/my_experiment/checkpoints/last.ckpt",   # LightlyTrain checkpoint
    data="my_data_dir",                                     # Directory with images
    format="torch",                                         # Embedding format
)
````

````{tab} Command Line
```bash
lightly-train embed out="my_embeddings.pth" checkpoint="out/my_experiment/checkpoints/last.ckpt" data="my_data_dir" format="torch"
````

The embeddings are saved to `my_embeddings.pth` and can be loaded like this:

```python
import torch

embeddings = torch.load("my_embeddings.pth")
embeddings["filenames"]     # List of filenames
embeddings["embeddings"]    # Tensor with embeddings with shape (num_images, embedding_dim)
```
