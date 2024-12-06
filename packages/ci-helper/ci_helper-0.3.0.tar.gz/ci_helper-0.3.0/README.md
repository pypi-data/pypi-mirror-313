# ci-helper

Output information to help build a Python package in CI

## Motivation

This tool exists to address certain issues of bit-rot and deployment of GitHub Actions
workflows (though the problem exists for CI generally) that build Python packages.

It looks up what current Python versions are supported so you can target them in your
builds without having to maintain a curated list. It determines whether building on
multiple OSs or Python versions is needed for a Python package, allowing you to deploy a
generic CI configuration for different types of packages without having to modify it for
each one specifically when they only vary in this way.

Specifically:

* It lists all stable and supported Python versions so your CI can target all supported
versions of Python without having to curate a manual list.

* It tells you what the second-most-recent minor version of Python is, so you can use that
as a sensible default for tools that require a recent-ish Python but are likely not to
work immediately after a new Python is released.

* It tells you whether a Python package is pure Python or not, so that your CI knows
whether it needs to build on multiple OSs/Python versions.

* It tells you whether a Python package's dependencies have environment markers or not, so
that your CI knows whether it needs to build on multiple OSs/Python versions, for
package formats that don't support environment markers in dependencies (e.g. conda
packages).

These functions are all serving the goals of:

* Minimising how often you need to modify your CI configs just because a new version of
  Python came our or an old version reached end-of-life
* Minimising (ideally to zero) how much you need to customise an otherwise generic CI
  config when you re-use it for different types of Python packages (e.g. pure vs impure)

## Installation

This package is available on PyPI, install it to your current Python environemnt with
```bash 
pip install ci-helper
```

## Usage:

```bash
# All stable, non-end-of-life Python versions:
$ ci-helper pythons
3.9,3.10,3.11,3.12,3.13

# Same but in the format used by `cibuildwheel`'s `CIBW_BUILD` environment variable (cpython-only for now):
$ ci-helper pythons --cibw
cp39-* cp310-* cp311-* cp312-* cp313-*

# The second-most recent minor Python release, a good choice for the version to run
# tools from:
$ ci-helper defaultpython
3.12

# Info about the source Python project in the current working directory - name, version,
# whether it's a pure Python package, and whether its build or run requirements contain
# any # environment markers (that is, whether its requirements vary by platform or
# Python version):
$ ci-helper distinfo .
{
    "name": "ci-helper",
    "version": "0.1.dev1+g5043fb5.d20241202",
    "is_pure": true,
    "has_env_markers": false
}

# Same but one field at a time, more convenient for assigning to environment variables:
$ ci-helper distinfo name .
ci-helper
$ ci-helper distinfo version .
0.1.0
$ ci-helper distinfo is_pure .
true
$ ci-helper distinfo has_env_markers .
false 
```

## Full help text

```shell
$ ci-helper -h
usage: ci-helper [-h] [--version] {pythons,defaultpython,distinfo} ...

positional arguments:
  {pythons,defaultpython,distinfo}
                        Action to perform
    pythons             Output list of stable Python versions that have not yet reached end of life, see `ci-helper pythons -h`
    defaultpython       Output the second-latest stable Python version in X.Y format, useful as a good choice for a default python version
    distinfo            Output info about the distribution, see `ci-helper distinfo -h`

options:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
```

```shell
$ ci-helper pythons -h
usage: ci-helper pythons [-h] [--cibw]

options:
  -h, --help  show this help message and exit
  --cibw      Output as a space-separated list in the format `cpXY-* cpXY-*` as appropriate for the CIBW_BUILD environment variable to build for all
              stable CPython versions, otherwise versions are output as a comma-separated list in the format X.Y,X.Y
```

```shell
$ ci-helper default_python -h
usage: ci-helper defaultpython [-h]

options:
  -h, --help  show this help message and exit
```

```shell
$ ci-helper distinfo -h
usage: ci-helper distinfo [-h]
                          [{name,version,is_pure,has_env_markers}]
                          project_directory

positional arguments:
  {name,version,is_pure,has_env_markers}
                        Name of field to output as a single json value, if not
                        given, all info is output as json
  project_directory     Directory of Python project

options:
  -h, --help            show this help message and exit
```

