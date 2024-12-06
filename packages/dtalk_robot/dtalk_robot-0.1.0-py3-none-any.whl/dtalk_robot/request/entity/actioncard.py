from dataclasses import dataclass, field
from typing import Self

from .btn import BtnBody


@dataclass
class ActionCardBody:
    hide_avatar: str = field(default=None)
    btn_orientation: str = field(default=None)
    single_url: str = field(default=None)
    single_title: str = field(default=None)
    text: str = field(default=None)
    title: str = field(default=None)
    btns: list[BtnBody] = field(default_factory=list)

    def add_btn(self: Self, btn: BtnBody) -> Self:
        self.btns.append(btn)
        return self

    def to_dict(self: Self) -> dict:
        return {
            "hideAvatar": self.hide_avatar,
            "btnOrientation": self.btn_orientation,
            "singleURL": self.single_url,
            "singleTitle": self.single_title,
            "text": self.text,
            "title": self.title,
            "btns": [btn.to_dict() for btn in self.btns],
        }
