from typing import List, Dict, Any, Tuple
import re
import mimetypes
from enum import IntEnum

from PIL import Image

from phound.chats.text_helpers import Tag, MessageTextFormat, MENTION_FORMAT


def parse_attachments(attachments: List[str]) -> List[Dict[str, Any]]:
    parsed_attachments = []
    for path in attachments:
        attachment = {"path": path, "type": _AttachmentType.FILE}
        mime_type, _ = mimetypes.guess_type(path)
        if mime_type:
            if mime_type.startswith("audio/"):
                attachment["type"] = _AttachmentType.SOUND
            elif mime_type.startswith("image/"):
                attachment["type"] = _AttachmentType.IMAGE
                with Image.open(path) as img:
                    attachment["dimentions"] = img.size
        parsed_attachments.append(attachment)
    return parsed_attachments


def extract_mentions(raw_text: str, text_format: MessageTextFormat) -> Tuple[str, List[Dict[str, int]]]:
    mentions = []
    text = raw_text
    for match in re.findall(MENTION_FORMAT.format(r"\d+", r".*?"), raw_text):
        persona_uid, label = re.findall(MENTION_FORMAT.format(r"(\d+)", r"(.*?)"), match)[0]
        if not label:
            label = persona_uid
        mentions.append({
            "uid": int(persona_uid),
            "offset": (text.find(match)
                       if text_format != MessageTextFormat.HTML
                       else _remove_html_tags(text).find(match)),
            "length": len(label)}
        )
        text = text.replace(match, label, 1)
    return text, mentions


def get_chat_id(from_uid: str, to_uid: str) -> str:
    return "".join([_uid_to_hex(i) for i in sorted([from_uid, to_uid])])


def _uid_to_hex(uid: str) -> str:
    hex_size = 16
    direct = hex(int(uid))[2:].upper().zfill(hex_size)
    chunk_size = 2
    return "".join(reversed([direct[i:i + chunk_size] for i in range(0, hex_size, chunk_size)]))


def _remove_html_tags(text: str) -> str:
    return re.sub(fr"<({'|'.join(list(Tag))})>(.*?)</\1>", r"\2", text)


class _AttachmentType(IntEnum):
    FILE = 1
    IMAGE = 2
    SOUND = 3
