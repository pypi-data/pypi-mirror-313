# Vitaleey CLI

> **NOTE:**
> When running this program, be aware that this only works with projects that are maintained and developed by Vitaleey.

## Installation

#### Poetry
```shell
poetry add vitaleey-cli
```

#### Pip
```shell
pip install vitaleey-cli
```

After installation run `vitaleey` to see the following:

```bash
Usage: vitaleey [OPTIONS] COMMAND [ARGS]...

  Vitaleey CLI tool

  This tool is used to interact with the Vitaleey API Gateway and
  Applications. If project isn't part of the group Vitaleey, the tool will not
  work.

Options:
  --version  Show the version and exit.
  --debug    Show debug logging
  --help     Show this message and exit.

Commands:
  api  API Gateway helper commands
  app  Application helper commands
```

### `pyproject.toml`

When using commands there are certain settings you can use. Each command has settings.

Example:
```toml
...
[tool.vitaleey.<command>]
...
```

> **NOTE:**
> This must be defined for using the CLI. If not defined even if it's empty you will not be able to use the program.

See below details about each setting.

## Commands

Each command has their own settings for in the `pyproject.toml`

### Application (`vitaleey app`)

`[tool.vitaleey.app]`

| Setting | Description | Default |
| ------ | ------ | ------ |
|`registry`|The registry to publish the application, options are `[gitlab, pypi]`|`gitlab`|
|`language`|The language of the application, options are `[python, react]`|`python`|
|`application_type`|The type of the application, options are `[package, microservice]`|`microservice`|

### API Gateway (`vitaleey api`)

#### All environments
`[tool.vitaleey.api_gateway]`

#### Environment specific
`[tool.vitaleey.api_gateway.env.(dev | acc | prod)]`

| Setting | Description | Default |
| ------ | ------ | ------ |
|`endpoint_dir`|The location where all the configurations for the gateway api can be found|`$PWD/config`|

#### Kubernetes

For Kubernetes you must have [kubectl](https://kubernetes.io/docs/reference/kubectl/) and [doctl]([https://docs.digitalocean.com/reference/doctl/how-to/install/]) installed.