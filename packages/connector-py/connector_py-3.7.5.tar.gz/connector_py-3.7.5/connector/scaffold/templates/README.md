# {title} Connector

[![PyPI - Version](https://img.shields.io/pypi/v/connector-{hyphenated_name}.svg)](https://pypi.org/project/connector-{hyphenated_name})
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/connector-{hyphenated_name}.svg)](https://pypi.org/project/connector-{hyphenated_name})

-----

## Table of Contents

- [Installation](#installation)
- [License](#license)

## Installation

If this connector is in the Lumos monorepo, ensure `connector-{hyphenated_name}` is added
to the top level `pyproject.toml` file. Otherwise:

```console
pip install connector-{hyphenated_name}[dev,fastapi]
```

If you want the HTTP server, `pip install connector-{hyphenated_name}[fastapi]`

If you're on Mac, you'll need to escape the square brackets in your ZSH shell:

```console
pip install connector-{hyphenated_name}\[dev,fastapi\]
```

## Usage

The package can be used in three ways:
1. A CLI to scaffold a custom connector with its own CLI to call commands
2. A library to create custom connector
3. A library to convert your custom connector code to a FastAPI HTTP server

To get started, run `{hyphenated_name} --help`

An example of running a command that accepts arguments:

```shell
{hyphenated_name} info --json '{{"a": 1}}'
```

### Hacking

There are some positional arguments under the "hacking" command for ease of development.

```console
{hyphenated_name} hacking --help
```

For instance, you can spin up a FastAPI server with the following command:

```console
{hyphenated_name} hacking http-server
```

If you navigate to http://localhost:8000/docs, you'll be able to run a Swagger UI to test your
endpoints.

## License

`connector-{hyphenated_name}` is distributed under the terms of the [Apache 2.0](./LICENSE.txt) license.
