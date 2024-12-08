# Alphaess-aio - a Alpha Open API client

## About

Sends get and post requests to available AlphaCloud API endpoints and retrieves data about you AlphaESS system.
Code generated out of API description.

## Prerequisites

Register account at https://open.alphaess.com/. You will recieve an AppID and AppSecret needed for authentification.

## How to use

```python
import asyncio
from alphaessaio import AlphaEssAPI, AlphaEssAuth

# setup auth
auth = AlphaEssAuth(appid="your_app_id", appsecret="your_app_secret")

#init api
alphaess_api = AlphaEssAPI(auth)

ess_list = asyncio.run(alphaess_api.get_ess_list())
```