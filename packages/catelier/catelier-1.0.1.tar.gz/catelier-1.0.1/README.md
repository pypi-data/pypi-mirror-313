# catelier

`catelier` is a Python package for decrypting data, using a custom atelier decryption algorithm implemented in C.

## Features

- Provides efficient atelier decryption functionality, based on C implementation.
- Supports Python 3.6+

## Installation

Install the latest version of `catelier` from PyPI:

```bash
pip install catelier
```

## Usage
```python
import catelier
data = b'...'
keyBytes = b'...'
nonceSeed = b'...'
dec = catelier.decrypt(data, keyBytes, nonceSeed)
