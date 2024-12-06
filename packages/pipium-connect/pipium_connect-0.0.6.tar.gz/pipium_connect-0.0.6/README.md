# Pipium Python connect

This is the package that connects Python models with the [Pipium](https://pipium.com) platform.

## Installation

```bash
pip install pipium-connect
```

## Code

```python
from pipium_connect import connect

connect(
    "your-securely-stored-api-key",
    {
      "hello_world": {
          "name": "Hello world!",
          "run_sync": lambda input: "Hello " + input["text"],
          "types": {
              "inputs": ["text/plain"],
              "output": "text/plain",
          },
      },
    }
)
```
