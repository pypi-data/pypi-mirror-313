from dataclasses import dataclass, field
from typing import Self


@dataclass
class TextBody:
    content: str = field(default=None)

    def to_dict(self: Self) -> dict:
        return {"content": self.content}
