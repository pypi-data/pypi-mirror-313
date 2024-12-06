from dataclasses import dataclass, field
from typing import Self


@dataclass
class AtBody:
    is_at_all: bool = field(default=None)
    at_mobiles: list[str] = field(default_factory=list)
    at_user_ids: list[str] = field(default_factory=list)

    def add_at_mobile(self: Self, mobile: str) -> Self:
        self.at_mobiles.append(mobile)
        return self

    def add_at_user_id(self: Self, user_id: str) -> Self:
        self.at_user_ids.append(user_id)
        return self

    def to_dict(self: Self) -> dict:
        return {
            "isAtAll": self.is_at_all,
            "atMobiles": self.at_mobiles,
            "atUserIds": self.at_user_ids,
        }
