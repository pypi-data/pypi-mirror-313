# Dappier Python SDK

The Dappier Python SDK provides an easy-to-use interface for interacting with the Dappier API.

---

## Installation

Install the SDK using pip:

```bash
pip install dappier
```

---

## Usage

Below is an example of how to use the Dappier SDK:

```python
import os
from dappier import Dappier

# Set your API key as an environment variable
os.environ["DAPPIER_API_KEY"] = "<YOUR_API_KEY>"

# Initialize the Dappier SDK
app = Dappier()

# Make an API call
response = app.real_time_search_api("Who won the US election in 2024?")
print(response.message)
```

Replace `<YOUR_API_KEY>` with your actual Dappier API key.

---

## Features

- **Real-time Search API:** Query real-world events and retrieve updated information.
- **Simple and Intuitive Interface:** Focused on ease of use and efficient API calls.

For detailed documentation and advanced features, refer to the official [Dappier documentation](https://docs.dappier.com/quickstart).
