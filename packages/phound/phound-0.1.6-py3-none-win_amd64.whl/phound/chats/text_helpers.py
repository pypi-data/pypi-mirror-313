from enum import Enum, IntEnum


MENTION_FORMAT = "<mention:persona_uid=\"{}\":label=\"{}\">"


class MessageTextFormat(IntEnum):
    PLAIN = 1
    HTML = 2
    GPTMARKDOWN = 3


class Tag(str, Enum):
    BOLD = "b"
    ITALIC = "i"
    UNDERLINE = "u"


def mention(persona_uid: str, label: str = "") -> str:
    return MENTION_FORMAT.format(persona_uid, label)


def bold(text: str) -> str:
    return _wrap(text, Tag.BOLD)


def italic(text: str) -> str:
    return _wrap(text, Tag.ITALIC)


def underline(text: str) -> str:
    return _wrap(text, Tag.UNDERLINE)


def _wrap(text: str, tag: Tag) -> str:
    return f"<{tag}>{text}</{tag}>"
