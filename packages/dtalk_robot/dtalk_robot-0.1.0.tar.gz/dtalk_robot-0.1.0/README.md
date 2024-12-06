# DingTalk Robot

This project is a DingTalk robot implemented using Python's aiohttp library.

## Features

- Asynchronous message handling
- Supports all message types

## Usage

```python
import asyncio

from dingtalk_robot import Robot
from dingtalk_robot.request import RequestBody, TextBody
from dingtalk_robot.response import ResponseBody

async def send(request_body: RequestBody) -> ResponseBody:
    async with Robot(access_token="access_token", secret="secret") as robot:
        return await robot.send_message(request_body)

text_msg: RequestBody = RequestBody.text_message(text=TextBody(content="Hello World!"))

response = asyncio.run(send(text_msg))

print(f"response[code={response.errcode}]: {response.errmsg}")
```
    