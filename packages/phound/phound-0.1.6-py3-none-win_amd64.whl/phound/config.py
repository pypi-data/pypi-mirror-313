import os
from dataclasses import dataclass

from dotenv import load_dotenv as _load_dotenv

_load_dotenv()

_DEFAULT_SBC = "wss://ow-sbc.phound.app/ucp"


@dataclass(frozen=True)
class Settings:
    sbc: str
    token: str
    personas: str
    phound_log: bool
    phound_log_dir: str

    def __post_init__(self) -> None:
        if not self.token or len(self.token.split(".")) != 2:
            raise ValueError("Token is invalid, must be in format <uid>.<api_key>")


settings = Settings(
    sbc=os.environ.get("SBC", _DEFAULT_SBC),
    token=os.environ.get("TOKEN", ""),
    personas=os.environ.get("PERSONAS", ""),
    phound_log=os.environ.get("PHOUND_LOG", "False").lower() == "true",
    phound_log_dir=os.environ.get("PHOUND_LOG_DIR", ""),
)
