# TM352 App

[![PyPI - Version](https://img.shields.io/pypi/v/tm352-app.svg)](https://pypi.org/project/tm352-app)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/tm352-app.svg)](https://pypi.org/project/tm352-app)
[![Test Status](https://stem-ts-gitlab.open.ac.uk/mmh352/tm352-app/badges/main/pipeline.svg)](https://stem-ts-gitlab.open.ac.uk/mmh352/tm352-app/-/pipelines)
[![Coverage](https://stem-ts-gitlab.open.ac.uk/mmh352/tm352-app/badges/main/coverage.svg)](https://stem-ts-gitlab.open.ac.uk/mmh352/tm352-app/-/tree/main)

A simple command-line application to support the practical activities and assessment in TM352.

-----

## Table of Contents

- [Installation](#installation)
- [Developer Setup](#developer-setup)
- [License](#license)

## Live Installation

For use in the VCE, the following command will install the package:

```console
$ pip install tm352-app
```

Then, to run it, use the following command:

```console
$ tm352
```

## Developer Setup

The development uses [hatch]() to manage dependencies and environments. To run the application in the development
environment use:

```console
$ hatch run tm352
```

Code styling is ensured using [pre-commit](https://pre-commit.com/). To install the necessary git hook to run the
checks at commit time, run:

```console
$ pre-commit install
```

## License

`TM352 App` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
