# Drax SDK for Python

Drax SDK for Python is a Python library that provides an easy way to interact with the Drax API. The SDK is built on top
of the Drax API and provides a simple interface to interact with the API.

## Installation

You can install the Drax SDK for Python using pip:

```bash
pip install drax-sdk
```

## Usage

### Initialize the Drax SDK

To use the Drax SDK, you need to initialize it with your API key. You can get your API key from the Drax dashboard.

```python
from drax_sdk.drax import Drax
from drax_sdk.model.config import DraxConfigParams

config = DraxConfigParams.standard(
    project_id="your_project_id",
    api_key="your_api_key",
    api_secret="your_api_secret"
)

drax = Drax(config)
```