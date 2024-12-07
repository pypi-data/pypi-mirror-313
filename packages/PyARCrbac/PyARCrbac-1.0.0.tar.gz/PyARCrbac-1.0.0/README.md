# PyARCrbac ![PyPI - Downloads](https://img.shields.io/pypi/dm/pyarcrbac) ![PyPI - Version](https://img.shields.io/pypi/v/pyarcrbac)
PyARCrbac is a Python library that provides functions for retrieving tokens from azure arc-enabled servers using the local metadata service. It can be used to obtain access tokens for Azure resources.
## Installation
```shell
pip3 install pyarcrbac
```
# Usage
Make sure you have the necessary permissions and environment variables set up to access the azure metadata service.
## Graph Tokens
Here's an example of how to use PyARCrbac to retrieve an graph access token:
```python
from pyarcrbac import pyrbac
import requests

def fetch_device_data():
  url = "https://graph.microsoft.com/v1.0/devices"
  headers = {"Authorization": f"Bearer {pyrbac.graph_token()}"}
  response = requests.get(url, headers=headers)
  return response.json()
```
## Azure Management Tokens
Here's an example of how to use PyARCrbac to retrieve an management access token:
```python
from pyarcrbac import pyrbac
import requests

def fetch_device_data():
  url = "https://management.azure.com/subscriptions"
  headers = {"Authorization": f"Bearer {pyrbac.mgmt_token()}"}
  response = requests.get(url, headers=headers)
  return response.json()
```


## Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License
This project is licensed under the MIT License.

## Contact
For any questions or inquiries, please open an issue.

## Disclaimer
I am not responsible for any damage and/or misuse as a result of using this lib.
