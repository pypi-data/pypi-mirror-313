from dataclasses import dataclass, field
from typing import Optional, Self

from .constants import MsgType
from .entity import (
    ActionCardBody,
    AtBody,
    FeedCardBody,
    LinkBody,
    MarkdownBody,
    TextBody,
)


@dataclass
class RequestBody:
    r"""DingTalk robot request body.

    see https://open.dingtalk.com/document/orgapp/custom-robots-send-group-messages
    """

    msgtype: MsgType
    text: TextBody = field(default=None)
    at: AtBody = field(default=None)
    link: LinkBody = field(default=None)
    markdown: MarkdownBody = field(default=None)
    action_card: ActionCardBody = field(default=None)
    feed_card: FeedCardBody = field(default=None)

    @classmethod
    def text_message(cls, text: TextBody, at: Optional[AtBody] = None) -> Self:
        return cls(msgtype=MsgType.TEXT, text=text, at=at)

    @classmethod
    def text_message_str(cls, content: str, at: Optional[AtBody] = None) -> Self:
        return cls(msgtype=MsgType.TEXT, text=TextBody(content=content), at=at)

    @classmethod
    def link_message(cls, link: LinkBody) -> Self:
        return cls(msgtype=MsgType.LINK, link=link)

    @classmethod
    def markdown_message(
        cls, markdown: MarkdownBody, at: Optional[AtBody] = None
    ) -> Self:
        return cls(msgtype=MsgType.MARKDOWN, markdown=markdown, at=at)

    @classmethod
    def action_card_message(cls, action_card: ActionCardBody) -> Self:
        return cls(msgtype=MsgType.ACTION_CARD, action_card=action_card)

    @classmethod
    def feed_card_message(cls, feed_card: FeedCardBody) -> Self:
        return cls(msgtype=MsgType.FEED_CARD, feed_card=feed_card)

    def to_dict(self: Self) -> dict:
        return {
            "msgtype": self.msgtype.value,
            "text": self.text.to_dict() if self.text else None,
            "at": self.at.to_dict() if self.at else None,
            "link": self.link.to_dict() if self.link else None,
            "markdown": self.markdown.to_dict() if self.markdown else None,
            "actionCard": self.action_card.to_dict() if self.action_card else None,
            "feedCard": self.feed_card.to_dict() if self.feed_card else None,
        }
