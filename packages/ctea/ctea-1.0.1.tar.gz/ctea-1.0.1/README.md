# ctea

`ctea` is a Python package for decrypting data, using a custom TEA decryption algorithm implemented in C.

## Features

- Provides efficient TEA decryption functionality, based on C implementation.
- Supports Python 3.6+

## Installation

Install the latest version of `ctea` from PyPI:

```bash
pip install ctea
```

## Usage
Here's how to use `ctea` for decryption:

```python
import ctea

dec = ctea.decrypt(data)
