# Sweepr

[![Python Lint](https://github.com/activatedgeek/sweepr/actions/workflows/lint.yml/badge.svg)](https://github.com/activatedgeek/sweepr/actions/workflows/lint.yml)

## Install

We use [`uv`](https://docs.astral.sh/uv/) to manage dependencies.

Install dependencies as:
```shell
uv sync --refresh --no-install-project --extra dev
```

Then install `sweepr` using

```shell
uv pip install -e .[dev]
```

## License

Apache 2.0
