# Watch DB

A simple Python package to get random watch information.

## Installation

```bash
pip install luxury_watches
```

## Usage

```python
from luxury_watches import get_watch, get_watch_name

# Get random watch details
watch = get_watch()
print(watch)  # Output: {'name': 'Submariner', 'brand': 'Rolex'}

# Get random formatted watch name
name = get_watch_name()
print(name)  # Output: 'Rolex Submariner'
```

## Command Line Usage

```bash
get-watch  # Prints a random watch name
```

## License

MIT

