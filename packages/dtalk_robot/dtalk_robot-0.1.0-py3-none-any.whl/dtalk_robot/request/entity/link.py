from dataclasses import dataclass, field
from typing import Self


@dataclass
class LinkBody:
    title: str = field(default=None)
    text: str = field(default=None)
    message_url: str = field(default=None)
    pic_url: str = field(default=None)

    def to_dict(self: Self) -> dict:
        return {
            "title": self.title,
            "text": self.text,
            "messageUrl": self.message_url,
            "picUrl": self.pic_url,
        }
