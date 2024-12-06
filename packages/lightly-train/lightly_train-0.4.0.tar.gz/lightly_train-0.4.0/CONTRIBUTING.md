# Contributing to LightlyTrain

## Development

```
git clone https://github.com/lightly-ai/lightly-train.git
make install-dev
```

```
make format
make static-checks
make test
```

### Documentation

Documentation is in the [docs](./docs) folder. To build the documentation, install
dev dependencies with `make install-dev`, then move to the `docs` folder and run:

```
make docs
```

This builds the documentation in the `docs/build/<version>` folder.

To build the documentation for the stable version, checkout the branch with the
stable version and run:

```
make docs-stable
```

This builds the documentaion in the `docs/build/stable` folder.

Docs can be served locally with:

```
make serve
```

#### Writing Documentation

The documentation source is in [docs/source](./docs/source). The documentation is
written in Markdown (MyST flavor). For more information regarding formatting, see:

- https://pradyunsg.me/furo/reference/
- https://myst-parser.readthedocs.io/en/latest/syntax/typography.html
