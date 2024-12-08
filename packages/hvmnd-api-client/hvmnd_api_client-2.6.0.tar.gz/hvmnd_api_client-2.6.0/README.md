# hvmnd api client

Python client library for the [Go API application](https://github.com/Smarandii/hvmnd-api).

## Installation

```bash
pip install hvmnd_api_client
```

## Usage

```py
from hvmnd_api_client import APIClient

client = APIClient(base_url='https://localhost/api/v1')

client.get_users()
client.get_nodes()
client.get_payments()
client.create_payment_ticket(user_id=1, amount=10000)
client.cancel_payment(id_='99999')

```