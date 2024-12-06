# Nanos

![logo](docs/source/_static/nanos_logo.png)

*Nanos* is a collection of small but handy python utilities: different
functions, classes and mixins. The library has zero dependencies and relies
only on built-in python modules.

Complete documentation: https://nanos.readthedocs.io/en/latest/index.html

## Features

* Utilities for working with data, dates, and time
* Formatters for various data types
* Logging and debugging tools
* Mixins for enhancing class functionality

## Installation

Library is available on PyPI and can be installed using pip:

```bash
pip install nanos
```

## Usage

For complete list of utilities, please refer to documentation:
https://nanos.readthedocs.io/en/latest/index.html

```python
from nanos import fmt

print(fmt.size(1024))  # Output: 1.00 KB
```

```python
import time
from nanos import time as ntime

with ntime.Timer() as t:
    time.sleep(2)

print(t.verbose())  # Output: 0:00:02.00
```

## License

The library is released under the [Apache License 2.0](LICENSE)
