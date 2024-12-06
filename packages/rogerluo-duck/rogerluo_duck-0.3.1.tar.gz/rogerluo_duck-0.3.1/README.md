# Duck - a package for the duck (operator learning) renormalization group

[![CI](https://github.com/Roger-luo/duck/actions/workflows/ci.yml/badge.svg)](https://github.com/Roger-luo/duck/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/Roger-luo/duck/graph/badge.svg?token=lFhrmt1PKc)](https://codecov.io/gh/Roger-luo/duck)

This package is a Python implementation of the duck (operator learning) renormalization group in JAX.

> [!NOTE]
> There was an older implementation of the duck RG in [teal](https://github.com/Roger-luo/teal), which
> was used for the first 2 versions of [the duck RG theory paper](https://arxiv.org/abs/2403.03199).

> [!IMPORTANT]
> This package is still under development in alpha stage, and the API may change in the future.

## Installation

This package is available on PyPI, thus can be installed via `pip`:

```bash
pip install rogerluo-duck
```

However, we highly recommend using [uv](https://docs.astral.sh/uv/) to install the package, run
the following in your Python project.

```bash
uv add rogerluo-duck
```

## Features

- a simple **symbolic system** for defining operators
- a set of **differentiable** local **solvers** defined on top of the above symbolic system
- implementation of the **duck RG** loss function
- a set of utilities for **training** and **evaluating** the machine learning model in the duck RG

## Documentation

The documentation is available at [https://rogerluo.dev/duck/](https://rogerluo.dev/duck/).

## License

This package is licensed under the Apache License 2.0.
