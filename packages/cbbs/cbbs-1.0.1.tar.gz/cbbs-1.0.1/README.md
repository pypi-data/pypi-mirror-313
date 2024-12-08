# cbbs

`cbbs` is a Python package for decrypting data, using a custom bbs decryption algorithm implemented in C.

## Features

- Provides efficient bbs decryption functionality, based on C implementation.
- Supports Python 3.6+

## Installation

Install the latest version of `cbbs` from PyPI:

```bash
pip install cbbs
```

## Usage
Here's how to use `cbbs` for decryption:

```python
import cbbs

dec = cbbs.decrypt(data)
