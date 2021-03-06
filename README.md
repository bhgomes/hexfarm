<div align="center">
<img src="https://raw.githubusercontent.com/bhgomes/hexfarm/master/docs/_static/ru_hex.png" alt="" width="400"/>

# hexfarm (_pre-α_)
_Rutgers HEX Computing Utility Library_

[![PyPI](https://img.shields.io/pypi/v/hexfarm.svg)](https://pypi.org/project/hexfarm)
[![Docs](https://readthedocs.org/projects/hexfarm/badge/)](http://hexfarm.readthedocs.io/en/stable/)
[![Build Status](https://travis-ci.com/bhgomes/hexfarm.svg?branch=master)](https://travis-ci.com/bhgomes/hexfarm)
[![Coverage Status](https://coveralls.io/repos/github/bhgomes/hexfarm/badge.svg?branch=master)](https://coveralls.io/github/bhgomes/hexfarm?branch=master)
[![Maintainability](https://api.codeclimate.com/v1/badges/88176f356ea8c698a18e/maintainability)](https://codeclimate.com/github/bhgomes/hexfarm/maintainability)
[![License](https://img.shields.io/github/license/bhgomes/hexfarm.svg?color=blue)](https://github.com/bhgomes/hexfarm/blob/master/LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

</div>


## Documentation

The documentation is hosted at [hexfarm.readthedocs.io](https://hexfarm.readthedocs.io). This is a WIP.


## Installation for Rutgers HEXCMS Users

See [`scripts/README.md`](scripts/README.md).


## Installing Development Environment

To install the development environment for `hexfarm` clone the repository and 
run the following

```bash
conda env update -f environment.yml --prune
conda activate hexfarm
```

To add the optional `ROOT` dependencies, run

```bash
conda env update -n hexfarm -f root-environment.yml
conda activate hexfarm
```

after initializing the `hexfarm` environment.

See [`scripts/README.md`](scripts/README.md) for more information on environments.


## License

This project is licensed under the [MIT Open Source License](LICENSE).

Copyright (c) 2019 Brandon Gomes 
