# QCI Client

## Getting started

### Installation

`qci-client` currently supports Python 3.8-12, inclusive, as specified in the
PEP-621-compliant pyproject.toml.

Install `qci-client` from the [public PyPI server](https://pypi.org/)
into your Python virtual environment using--

```bash
pip install qci-client
```

### Instantiating a Client for Optimization

#### With Environment Variables

To access the API, set these environment variables--

<!-- markdown-link-check-disable-next-line -->
- QCI_API_URL - URL for Qatalyst API, Example: "https://api.qci-prod.com"
- QCI_TOKEN - refresh token string for securely accessing Qatalyst API

then instantiate a `QciClient` as follows--

```python
# An alias for `from qci_client.optimization.client import Client as QciClient`.
from qci_client import QciClient

client = QciClient()
```

#### Without Environment Variables

Access the API without first defining environment variables by instantiating a
`QciClient` as follows--

```python
# A alias for `from qci_client.optimization.client import Client as QciClient`.
from qci_client import QciClient

client = QciClient(url="https://api.qci-prod.com", api_token="<secret-token>")
```
