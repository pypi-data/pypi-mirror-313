from dataclasses import dataclass, field
from typing import Self


@dataclass
class FeedCardLinkBody:
    pic_url: str = field(default=None)
    message_url: str = field(default=None)
    title: str = field(default=None)

    def to_dict(self: Self) -> dict:
        return {
            "picURL": self.pic_url,
            "messageURL": self.message_url,
            "title": self.title,
        }


@dataclass
class FeedCardBody:
    links: list[FeedCardLinkBody] = field(default_factory=list)

    def add_link(self: Self, link: FeedCardLinkBody) -> Self:
        self.links.append(link)
        return self

    def to_dict(self: Self) -> dict:
        return {"links": [link.to_dict() for link in self.links]}
