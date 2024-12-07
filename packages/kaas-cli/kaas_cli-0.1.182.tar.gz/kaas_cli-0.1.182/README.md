# KaaS CLI

## Simple Installation
Our deployments can be found on [Pypi](https://pypi.org/project/kaas-cli/).

### Installation
`pip install --user kaas-cli`
or 
`sudo pip install kaas-cli`

## For Developers

Prerequisites: `python >= 3.10`, `pip >= 20.0.2`, `poetry >= 1.3.2`.

### Installation

To install the package using `pip`, start by building from [Source](https://github.com/runtimeverification/kaas)

```bash
make build
pip install dist/*.whl
```

Configure the CLI by copying the example environment file and setting up the necessary environment variables:

```bash
cp .flaskenv.example .flaskenv
```

Then, edit the `.flaskenv` file to match your settings.

### Environment Variables

Here's an overview of the environment variables:

- **SERVER_URL**: The KaaS server API address for the main interaction within the CLI tool. This is a required field. For local development, use `http://localhost:5000`.
- **DEFAULT_DIRECTORY**: The folder path for artifacts. This is an optional field. You can leave it empty.
- **DEFAULT_VAULT_ID**: Artifacts should be associated with a project ID. This is an optional field. You can leave it empty.
- **DEFAULT_KEY**: If the user is not the owner of the project, they are required to provide a security key. This is an optional field. You can leave it empty.

### Usage

After installing the dependencies with `poetry install`, you can spawn a shell using `poetry shell`, or alternatively, use `make`:

```bash
make shell
kaas-cli hello
kaas-cli --version
```

VAULT_SPEC is an important definition. This is used to access specific organizations and vaults with permission control limitng what tokens have access to. 

The spec follows the form of 
```
organization/vault_name
```

To verify the installation, run `kaas-cli hello`. If you see the message `Hello World!`, the CLI is set up correctly.

### Documentation

For detailed usage instructions of the `kaas-cli` tool, please refer to the official [documentation](https://docs.runtimeverification.com/kaas/guides/getting-started).
