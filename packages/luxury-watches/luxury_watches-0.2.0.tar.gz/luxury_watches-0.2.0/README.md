# Watch DB

A simple Python package to get random watch information.

## Installation```bash
pip install tractor_db
```

## Usage

```python
from tractor_db import get_tractor, get_tractor_name

# Get random tractor details
tractor = get_tractor()
print(tractor)  # Output: {'name': 'L3901', 'brand': 'Kubota'}

# Get random formatted tractor name
name = get_tractor_name()
print(name)  # Output: 'Kubota L3901'
```

## Command Line Usage

```bash
tractor-db  # Prints a random tractor name
```

## License

MIT

