# Maintaining LightlyTrain

This document is intended for maintainers of Lightly**Train**. If you would like to
contribute, please refer to the [CONTRIBUTING.md](CONTRIBUTING.md) document.

## Release

Follow these steps to release a new version of Lightly**Train**:

1. Rewrite the unreleased part of the [CHANGELOG.md](CHANGELOG.md) into nicely digestible information.
1. Bump the version in `lightly_train/__init__.py`. We use [Semantic Versioning](https://semver.org/). Note that we are still on major version 0 and therefore minor version
   bumps are considered breaking changes.
1. Once the version is bumped, create a new release on GitHub: https://github.com/lightly-ai/lightly-train/releases with a new tag that matches the version number. Make sure to
   create release notes using the "Generate release notes" button.
1. To release on PyPI, run the [Release PyPI action](https://github.com/lightly-ai/lightly-train/actions/workflows/release_pypi.yml) from the main branch.
1. To release on DockerHub, run the [Release DockerHub action](https://github.com/lightly-ai/lightly-train/actions/workflows/release_dockerhub.yml) from the branch with the new
   version tag.
1. To release the documentation, run the [Release Documentation](https://github.com/lightly-ai/lightly-train/actions/workflows/release_documentation.yml) from the main branch.
1. If the README was updated, make sure to copy the information to the DockerHub
   description for Lightly**Train**: https://hub.docker.com/r/lightly/ (you might have to ask
   someone who is a member of the Lightly DockerHub organization to do this for you).
