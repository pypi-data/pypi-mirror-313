# Changelog

All notable changes to Lightly**Train** will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## \[Unreleased\]

### Added

### Changed

### Deprecated

### Removed

### Fixed

### Security

## \[0.4.0\] - 2024-12-05

### Added

- Log system information during training
- Add [Performance Tuning guide](https://docs.lightly.ai/train/stable/performance/index.html)
  with documentation for [multi-GPU](https://docs.lightly.ai/train/stable/performance/multi_gpu.html)
  and [multi-node](https://docs.lightly.ai/train/stable/performance/multi_node.html) training
- Add [Pillow-SIMD support](https://docs.lightly.ai/train/stable/performance/index.html#dataloader-bottleneck-cpu-bound)
  for faster data processing
  - The docker image now has Pillow-SIMD installed by default
- Add [`ultralytics`](https://docs.lightly.ai/train/stable/export.html#format) export format
- Add support for DINO weight decay schedule
- Add support for SGD optimizer with `optim="sgd"`
- Report final `accelerator`, `num_devices`, and `strategy` in the resolved config
- Add [Changelog](https://docs.lightly.ai/train/stable/changelog.html) to the documentation

### Changed

- Various improvements for the DenseCL method
  - Increase default memory bank size
  - Update local loss calculation
- Custom models have a [new interface](https://docs.lightly.ai/train/stable/models/custom_models.html#custom-models)
- The number of warmup epochs is now set to 10% of the training epochs for runs with less than 100 epochs
- Update default optimizer settings
  - SGD is now the default optimizer
  - Improve default learning rate and weight decay values
- Improve automatic `num_workers` calculation
- The SPPF layer of Ultralytics YOLO models is no longer trained

### Removed

- Remove DenseCLDINO method
- Remove DINO `teacher_freeze_last_layer_epochs` argument

## \[0.3.2\] - 2024-11-06

### Added

- Log data loading and forward/backward pass time as `data_time` and `batch_time`
- Batch size is now more uniformly handled

### Changed

- The custom model `feature_dim` property is now a method
- Replace FeatureExtractor base class by the set of Protocols

### Fixed

- Datasets support symlinks again

## \[0.3.1\] - 2024-10-29

### Added

- The documentation is now available at https://docs.lightly.ai/train
- Support loading checkpoint weights with the `checkpoint` argument
- Log resolved training config to tensorboard and WandB

### Fixed

- Support single-channel images by converting them to RGB
- Log config instead of locals
- Skip pooling in DenseCLDino

## \[0.3.0\] - 2024-10-22

### Added

- Add Ultralytics model support
- Add SuperGradients PP-LiteSeg model support
- Save normalization transform arguments in checkpoints and automatically use them
  in the embed command
- Better argument validation
- Automatically configure `num_workers` based on available CPU cores
- Add faster and more memory efficient image dataset
- Log more image augmentations
- Log resolved config for CallbackArgs, LoggerArgs, MethodArgs, MethodTransformArgs, and OptimizerArgs
