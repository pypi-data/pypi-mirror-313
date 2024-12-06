from enum import StrEnum


class MsgType(StrEnum):
    TEXT = "text"
    LINK = "link"
    MARKDOWN = "markdown"
    ACTION_CARD = "actionCard"
    FEED_CARD = "feedCard"
