# Etui
Exquisite capsule fitted with useful helpers for every day coding.
**Etui** provides simple, yet powerful, functions that are otherwise absence.

## Installation
```shell
pip install etui
```


## Examples
```python
from etui import is_json

s = '{"id": 0, "name": "Test"}'
print(is_json(s))

> True

s = 'Hello Pluto!'
print(is_json(s))

> False
```

## REST
### Paginator
Function to fully query API with Paginated Results
```python
import requests
from etui import rest

url = 'https://api.example.com'
p = {'fields': 'accounts', 'limit': 100}

req = requests.get(url, params=p)

# Avalable data exceeds limit and endpoint needs to be called multiple times
complete_data = paginator(req, 'data', ['paging', 'next']) 

print('Accounts: {len(complete_data)}')

> 'Accounts: 26023'
```

## ENCRYPT / DECRYPT
```python
from etui import encrypt_decrypt as ende
encrypted = ende.encrypt("Hello Encrypted World")
decrypted = ende.decrypt(encrypted)
