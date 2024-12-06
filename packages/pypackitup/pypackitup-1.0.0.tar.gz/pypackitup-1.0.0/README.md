# pypackitup - Python Package Template

Template repository for developing Python packages.

[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/wrencode/pypackitup?color=yellowgreen&label=latest%20release&sort=semver)](https://github.com/wrencode/pypackitup/releases/latest)
[![GitHub tag (latest SemVer)](https://img.shields.io/github/v/tag/wrencode/pypackitup?color=yellowgreen&label=latest%20version&sort=semver)](https://github.com/wrencode/pypackitup/tags)
[![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/wrencode/pypackitup/python-package.yml?color=brightgreen&label=build)](https://github.com/wrencode/pypackitup/actions/workflows/python-package.yml)

[![PyPI](https://img.shields.io/pypi/v/pypackitup.svg?style=flat)](https://pypi.python.org/pypi/pypackitup)
[![PyPI](https://img.shields.io/pypi/dm/pypackitup.svg?style=flat)](https://pypi.python.org/pypi/pypackitup)
[![PyPI](https://img.shields.io/pypi/pyversions/pypackitup.svg?style=flat)](https://pypi.python.org/pypi/pypackitup)
[![PyPI](https://img.shields.io/pypi/l/pypackitup.svg?style=flat)](https://pypi.python.org/pypi/pypackitup)

---

<sub>***Do you like the Python Package Template? Star the repository on GitHub and please consider helping support its ongoing development:***</sub>

[<img src="https://raw.githubusercontent.com/wrencode/pypackitup/refs/heads/main/docs/wrencode-donation-venmo-qr-code.jpg" width="300"/>](https://venmo.com/wrencode?txn=pay)

<!-- https://venmo.com/<USER_NAME_1>,<USER_NAME_2>...?txn=<charge|pay>&note=<NOTE>&amount=<AMOUNT> -->

---

<div class="hide-next-element"></div>

**[READ THE DOCS HERE!](https://pypackitup.wrencode.dev)**
<br/>
<sup>Detailed documentation can be found at [https://pypackitup.wrencode.dev](https://pypackitup.wrencode.dev).</sup>

<div class="hide-next-element"></div>

&nbsp;

<div class="hide-next-element"></div>

### Table of Contents

<div class="hide-next-element"></div>

* [About](#about)
    * [Dependencies](#dependencies)
    * [Toolchain](#toolchain)
* [Setup](#setup)
    * [Configuration](#configuration)
    * [Version Control](#version-control)
    * [Documentation](#documentation)
    * [Environment](#environment)
    * [Code](#code)

<div class="hide-next-element"></div>

---

<a name="about"></a>
### About

The Python Package Template is an example for Python package development.

<a name="dependencies"></a>
#### Dependencies

The Python Package Template does not have any third-party dependencies to run the code. It has several development dependencies, which can be seen in the package `pyproject.toml`.

<a name="toolchain"></a>
#### Toolchain

The below tools and resources are used as part of pypackitup:

* [uv](https://github.com/astral-sh/uv) - package management
* [ruff](https://github.com/astral-sh/ruff) - code linting
* [bandit](https://bandit.readthedocs.io/en/latest/) - code security
* [make](https://www.gnu.org/software/make/manual/make.html) - Makefile build automation
* [MkDocs](https://www.mkdocs.org) - package documentation
* [python-dotenv](https://github.com/theskumar/python-dotenv) - programmatic access to environment variables defined in a `.env` file
* [pytest](https://docs.pytest.org/en/stable/) - code testing framework
* [GitHub Actions](https://docs.github.com/en/actions) - CI/CD
* [act](https://github.com/nektos/act) - GitHub Actions testing

---

<a name="setup"></a>
### Setup

The below list covers all updates needed in the Python Package Template when using it to create a new Python package:

<a name="configuration"></a>
#### Configuration

* `pyproject.toml`: Update all relevant fields as needed for the new package.

<a name="version-control"></a>
#### Version Control

* `.gitignore`: Add any package-specific files that should not be checked in to version control.
* `.github/ISSUE_TEMPLATE/`: Make any package-specific changes to the project issue templates.
* `.github/workflows/python-package.yml`: Update the supported Python versions and add any necessary CI/CD steps.

<a name="documentation"></a>
#### Documentation

* `README.md`: Update the `README.md` with all necessary package documentation.
* `mkdocs.yml`: Update the `nav` section with all necessary pages and their corresponding Markdown files (see below).
* `docs-mkdocs/CNAME`: Update the `CNAME` file with the desired mkdocs documentation GitHub Pages custom domain.
* `docs-mkdocs/extra.css`: Add any custom CSS for the mkdocs documentation.
* `docs-mkdocs/extra.js`: Add any custom JavaScript for the mkdocs documentation.
* `docs-mkdocs/*.md`: Add any necessary Markdown (`.md`) files for pages in the mkdocs documentation.
* `docs-mkdocs/*.svg/*.png/*.jpg/etc.`: Add any necessary images for the mkdocs documentation.

<a name="environment"></a>
#### Environment

* `.env`: Create a `.env` file from the provided `.env.template` file (run `cp .env.template .env` in the command line) and add any necessary package environment variables.

<a name="code"></a>
#### Code

* `src/pypackitup/`: Rename the source code directory to match the project directory and follow the [PEP naming conventions](https://peps.python.org/pep-0008/#package-and-module-names) for the package.
* `src/pypackitup/__init__.py`: Update the package `__init__.py` with available imports.
* `src/pypackitup/*.py`: Add package code.
* `tests/`: Add tests for package code.
