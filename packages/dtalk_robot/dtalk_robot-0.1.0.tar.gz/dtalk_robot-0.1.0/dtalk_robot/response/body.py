from dataclasses import dataclass, field


@dataclass
class ResponseBody:
    r"""DingTalk response body.

    see: https://open.dingtalk.com/document/orgapp/custom-robots-send-group-messages
    """

    errmsg: str = field(default=None)
    errcode: int = field(default=None)
