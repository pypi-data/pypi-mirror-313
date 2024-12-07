# Epistemix Platform Client
For users of the epx client please visit our [documentation](https://docs.epsitemix.com/epx-client-docs/)

# Epistemix Platform Client Developers Guide

Client for running simulations with Epistemix Platform Cloud.

## Branching Strategy

This repo follows the environment strategy described
[here](https://github.com/Epistemix-Inc/poc-gitlabflow-release).

## Development

### Initial setup

To bootstrap the development environment using a Python virtual environment,
run

```shell
. scripts/setup
```

This will create and activate the development Python environment. This
environment can be reactivated subsequently in a different shell session with

```shell
source .venv/bin/activate
```

### Pre-commit

Before committing, developers are asked to run the following scripts and resolve
any identified issues:

```shell
scripts/test
scripts/format
scripts/lint
```

### Test data generation

Test data is generated in the `scripts/test/tests` directory. Note that the
test data is checked into this repo and should only need to be regenerated
if the generation script needs to be changed. See `resources/tests/README.md`
for more details.

### Testing integration with SRS

The best known way to test `epx_client`'s interaction with SRS is to package
it up, install it in the Platform, and perform manual testing in-situ. This
can be done by following these steps:

#### 1. Build the Program


Checkout the feature branch that you want to build. Make sure you are in a virtual
environment (see [initial setup](#initial-setup)). Build the epx python package:

```shell
python -m build
```

This will create package artifacts in the `/dist` directory.

#### 2. Upload the Artifact to Platform

Within the Platform environment that you wish to test in, click the upload file
button from the file menu. Upload the built `.tar.gz` artifact from your local
`/dist` directory.

<img src="./img/upload-button.png" alt="upload button" width="250"/>

#### 3. Install `epx_client` on the Platform

Use `pip` to install the artifact on the Platform. E.g. if your build artifact
is called `~/packages/epx-0.0.0+unknown.tar.gz`, run

```shell
python -m pip install --user --force-reinstall ~/packages/epx-0.0.0+unknown.tar.gz
```
This can be done either using the Platform terminal, or from within a notebook.

`--force-reinstall` forces pip to install the most recently uploaded package artifact.

#### 4. Perform manual tests as required

#### 5. Revert back to default version of epx

To reset your Platform IDE to use the originally installed version of `epx_client`, uninstall
`epx_client`. Since the testing version was installed for your user account only (`--user`),
the globally installed version will show as the installed version.

```shell
python -m pip uninstall epx -y
```

## Documentation

Documentation for the package uses the [Sphinx](https://www.sphinx-doc.org)
framework in the `docs` directory. To build and locally host the docs at port
`8000` run

```shell
scripts/docs
```

## Making a Release

To make a release, follow the process described [here.](https://github.com/Epistemix-com/poc-gitlabflow-release?tab=readme-ov-file#releasing-to-production)