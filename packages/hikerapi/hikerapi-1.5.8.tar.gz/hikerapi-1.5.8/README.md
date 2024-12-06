# Hikerapi client, for Python 3

## Installation

```
pip install hikerapi
```

## Usage

Create a token https://hikerapi.com/tokens and copy "Access key"

```python
from hikerapi import Client

cl = Client(token="<ACCESS_KEY>")
user = cl.user_by_username_v2("instagram")
print(user)
```

```python
from hikerapi import AsyncClient

cl = AsyncClient(token="<ACCESS_KEY>")
user = await cl.user_by_username_v2("instagram")
print(user)
```

## Run tests

```
HIKERAPI_TOKEN=<token> pytest -v tests.py

HIKERAPI_TOKEN=<token> pytest -v tests.py::test_search_music
```