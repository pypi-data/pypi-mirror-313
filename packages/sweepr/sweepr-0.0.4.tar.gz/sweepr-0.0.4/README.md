# Sweepr

[![Python Lint](https://github.com/activatedgeek/sweepr/actions/workflows/lint.yml/badge.svg)](https://github.com/activatedgeek/sweepr/actions/workflows/lint.yml) [![Publish PyPI](https://github.com/activatedgeek/sweepr/actions/workflows/publish.yml/badge.svg?event=release)](https://github.com/activatedgeek/sweepr/actions/workflows/publish.yml)

## Install

```shell
pip install sweepr
```

## Development

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

Apache License 2.0
