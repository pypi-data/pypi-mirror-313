# Getting started

## Requirements

The **EasyCrystallography** library is developed in Python, so Python must be
installed on your system. The library is compatible with Python versions 3.9
through 3.12.

## Environment setup <small>optional</small> { #environment-setup data-toc-label="Environment setup" }

We recommend using a virtual environment – an isolated Python runtime where any
packages you install or update are contained within that environment. If you
encounter issues, you can simply delete and recreate the environment. Setting it
up is straightforward:

Create a new virtual environment with:

```console
python3 -m venv venv
```

<!-- prettier-ignore-start -->
Activate the environment with:

=== ":material-apple: macOS"
    ```console
    . venv/bin/activate
    ```
=== ":fontawesome-brands-windows: Windows"
    ```console
    . venv/Scripts/activate
    ```
=== ":material-linux: Linux"
    ```console
    . venv/bin/activate
    ```
<!-- prettier-ignore-end -->

Your terminal should now print `(venv)` before the prompt, which is how you know
that you are inside the virtual environment that you just created.

Exit the environment with:

```console
deactivate
```

## Installation

### From PyPI <small>recommended</small> { #from-pypi data-toc-label="From PyPI" }

**EasyCrystallography** is published on the Python Package Index (PyPI)
repository and can be installed with the package installer for Python (pip),
ideally by using a [virtual environment](#environment-setup). To do so, use the
following command:

```console
pip install 'easycrystallography'
```

To install a specific version of EasyDiffraction, e.g. 0.6.0, use:

```console
pip install 'easycrystallography==0.6.0'
```

Upgrading to the latest version can be done with:

```console
pip install --upgrade --force-reinstall easycrystallography
```

To show the currently installed version, use:

```console
pip show easycrystallography
```

### From GitHub

Installing an unreleased version is not recommended and should only be done for
testing purposes.

Here is an example of how to install **EasyCrystallography** directly from our
GitHub repository, e.g., from the `develop` branch:

```console
pip install git+https://github.com/EasyScience/EasyCrystallography@develop
```
