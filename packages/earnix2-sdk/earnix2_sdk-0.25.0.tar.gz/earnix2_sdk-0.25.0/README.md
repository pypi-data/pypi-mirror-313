## Earnix 2.0 SDK

[![ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://github.com/python/mypy)
[![bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)

**Earnix is a global provider of Intelligent Insurance and Banking Operations through agile, composable and real-time solutions.**

This is a Software Development Kit for interactions with the Earnix 2.0 line of products, providing HTTP clients and models covering 100% of the backend's capabilities, wrapped in an easy-to-use package. As of now, we only offer 1:1 interactions with the backend APIs, but we plan to introduce custom flows that call multiple APIs in the future.

With this package, you don't need to be learning the APIs, implementing the HTTP protocol or managing JSONs. For the best experience, we recommend using it with a modern Python LSP/IDE. We try to use type hinting whenever possible. The full developer experience includes automatic OOP model hierarchies, code completion, field validations and more.

## Requirements

- Python >= 3.9.
- An Earnix 2.0 account.
- A token, linked to that account.

## Installation

- Using `pip` (maybe inside a `venv`):

  ```shell
  pip install earnix2-sdk
  ```

- Using a specific Python:

  ```shell
  python3.10 -m pip install earnix2-sdk
  ```

- Using another tool (such as `pdm` or `poetry`):

  ```shell
  pdm add earnix2-sdk
  ```

> In macOS, if your Python was installed with `brew` and you encounter SSL errors (this is unrelated to Earnix):  
> `/Applications/Python*/Install\ Certificates.command`

## Example usage

- Print your Connections:

  ```python
  from earnix2_sdk.core import ConnectionService

  connection_service = ConnectionService(
    server="eu",
    token="...",
  )

  connections = connection_service.list_connections()
  print(connections)
  ```
