import base64
import hashlib
import hmac
import time
import urllib.parse
from types import TracebackType
from typing import Final, Optional, Self, Type

import aiohttp

from .request import RequestBody
from .response import ResponseBody


class Robot:
    r"""DingTalk robot client. Support async context manager."""

    DINGTALK_ROBOT_SEND_URL: Final[str] = "https://oapi.dingtalk.com/robot/send"

    def __init__(self: Self, access_token: str, secret: str) -> None:
        self.__access_token = access_token
        self.__secret = secret
        self.__session = aiohttp.ClientSession()

    @staticmethod
    def dingtalk_robot_sign(timestamp: int, secret: str) -> str:
        r"""Generate DingTalk robot sign.

        see https://open.dingtalk.com/document/orgapp/customize-robot-security-settings

        :param timestamp: timestamp
        :param secret: secret

        :return: sign
        """
        secret_enc = secret.encode("utf-8")

        string_to_sign = f"{timestamp}\n{secret}"
        string_to_sign_enc = string_to_sign.encode("utf-8")
        hmac_code = hmac.new(
            secret_enc, string_to_sign_enc, digestmod=hashlib.sha256
        ).digest()

        return urllib.parse.quote_plus(base64.b64encode(hmac_code))

    @classmethod
    def build_dingtalk_robot_send_url(
        cls, access_token: str, secret: Optional[str] = None
    ) -> str:
        r"""Build DingTalk robot webhook url.

        You need to make sure that secret is None or not before calling this method.

        :param access_token: access token
        :param secret: secret

        :return: webhook url
        """
        if secret is None or secret.strip() == "":
            return f"{cls.DINGTALK_ROBOT_SEND_URL}?access_token={access_token}"

        timestamp = round(time.time() * 1000)
        _sign = cls.dingtalk_robot_sign(timestamp, secret)

        return f"{cls.DINGTALK_ROBOT_SEND_URL}?access_token={access_token}&timestamp={timestamp}&sign={_sign}"

    async def send_message(self: Self, send_body: RequestBody) -> ResponseBody:
        url = self.build_dingtalk_robot_send_url(self.__access_token, self.__secret)

        async with self.__session.post(url, json=send_body.to_dict()) as response:
            response_json = await response.json()
            return ResponseBody(
                errmsg=response_json.get("errmsg"), errcode=response_json.get("errcode")
            )

    async def close(self: Self) -> None:
        await self.__session.close()

    async def __aenter__(self: Self) -> Self:
        return self

    async def __aexit__(
        self: Self,
        exc_type: Type[BaseException],
        exc_val: BaseException,
        exc_tb: TracebackType,
    ) -> None:
        await self.close()
