from dataclasses import dataclass, field
from typing import Self


@dataclass
class BtnBody:
    action_url: str = field(default=None)
    title: str = field(default=None)

    def to_dict(self: Self) -> dict:
        return {"actionURL": self.action_url, "title": self.title}
