from enum import StrEnum
from enum import auto as enum_auto


class ApiSpec(StrEnum):

    auto = enum_auto()
    kserve_v1 = enum_auto()
    kserve_v2 = enum_auto()
    openai_completion_v1 = enum_auto()
    openai_chat_completion_v1 = enum_auto()

    @classmethod
    def _missing_(cls, value: str):
        value = value.lower()
        for member in cls:
            if member.value == value:
                return member
        return None
