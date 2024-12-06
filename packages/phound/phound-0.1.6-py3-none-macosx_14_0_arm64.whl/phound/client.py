import json
import os
import subprocess
import threading
from pathlib import Path
from typing import Any, Dict, List, Optional, TextIO, cast

from phound.config import settings
from phound.event_listener import EventListener
from phound.events import Event, EventType
from phound.logging import get_logging_parameters, logger

_DEFAULT_CHANNEL_ID = "0"
_HEALTH_CHECK_INTERVAL_SECONDS = 5
lock = threading.Lock()


class PhoundPopen(subprocess.Popen):
    stdin: TextIO
    stdout: TextIO


class Client:
    def __init__(self) -> None:
        self._process = self._create_process()
        self._event_listener = EventListener(self._process.stdout)
        self._connect()

        self._health_check_thread = _HealthCheckThread(target=self._restart_not_running_process)
        self._health_check_thread.start()

        self._channels_enabled = False
        self._channels_port = 0

    def stop(self) -> None:
        self._health_check_thread.stop()
        self._health_check_thread.join()
        self._destroy_process()

    def send_message(self,
                     persona_uid: str,
                     chat_id: str,
                     text: str,
                     text_format: int,
                     attachments: Optional[List[Dict[str, Any]]] = None,
                     mentions: Optional[List[Dict[str, int]]] = None,
                     app_meta: Optional[Dict[str, Any]] = None,
                     channel_id: str = _DEFAULT_CHANNEL_ID,
                     wait_sent: bool = True,
                     **kwargs: Any) -> None:
        message_json = {
            "text": text,
            "chan": channel_id,
            "wait": wait_sent,
            "format": text_format,
            **kwargs,
        }
        if attachments:
            message_json["attachments"] = json.dumps(attachments)
        if mentions:
            message_json["mentions"] = json.dumps(mentions)
        if app_meta:
            message_json["app_meta"] = json.dumps(app_meta)
        self._write(f"send-message {persona_uid} {chat_id} {channel_id} <<JSON\n{json.dumps(message_json)}")

    def wipe_message(self,
                     persona_uid: str,
                     chat_id: str,
                     message_id: str,
                     channel_id: str = _DEFAULT_CHANNEL_ID) -> None:
        self._write(f"wipe-message {persona_uid} {chat_id} {message_id} {channel_id}")

    def make_call(self, persona_uid: str, phone_number: str) -> None:
        self._write(f"call {persona_uid} {phone_number}")

    def answer_call(self, call_id: str) -> None:
        self._write(f"answer {call_id}")

    def delay_call(self, call_id: str, milliseconds: int) -> None:
        self._write(f"delay {call_id} {milliseconds}")

    def record_call(
        self,
        call_id: str,
        file_path: str,
        min_chunk_len: int = 0,
        max_chunk_len: int = 0,
        chunk_overlap: int = 0
    ) -> None:
        cmd = f"record {call_id} {file_path}"
        if min_chunk_len and max_chunk_len:
            cmd += f" sgm:{min_chunk_len}:{max_chunk_len}:{chunk_overlap}"
        self._write(cmd)

    def play_file(self, call_id: str, file_path: str) -> None:
        self._write(f"play {call_id} {file_path}")

    def hangup(self, call_id: str) -> None:
        self._write(f"hangup {call_id}")

    def show_typing(
        self, persona_uid: str, chat_id: str, timeout: int = 10, channel_id: str = _DEFAULT_CHANNEL_ID
    ) -> None:
        self._write(f"typing-indicator {persona_uid} {chat_id} {timeout} {channel_id}")

    def request_chat_history(
        self,
        persona_uid: str,
        chat_id: str,
        start_message_id: str,
        channel_id: str = _DEFAULT_CHANNEL_ID,
        depth: int = 10
    ) -> None:
        self._write(f"get-history-bulk {persona_uid} {chat_id} {start_message_id} {channel_id} {depth}")

    def lookup_phone_number(self, phone_number: str, channel_id: str = _DEFAULT_CHANNEL_ID) -> None:
        self._write(f"lookup-phone-number {phone_number} {channel_id}")

    def request_next_event(self, channel_id: str) -> None:
        self._write(f"pump-queue {channel_id}")

    def wait_event(self, *event_types: EventType) -> Event:
        return self._event_listener.wait_event(*event_types)

    def shutdown(self) -> None:
        self._write("shutdown")

    def enable_channels(self, port: int) -> None:
        self._channels_enabled = True
        self._channels_port = port
        self._write(f"set-handler channel 127.0.0.1:{port}")

    def listen_dtmf(self, call_id: str) -> None:
        self._write(f"listen-dtmf {call_id}")

    def send_dtmf(self, call_id: str, dtmf: str) -> None:
        self._write(f"dtmf {call_id} {dtmf}")

    def _connect(self) -> None:
        uid, api_key = settings.token.split(".")
        self._write(f"connect {settings.sbc} {uid} {api_key} {settings.personas}", log=False)
        while True:
            event = self._event_listener.wait_event()
            if event.type == EventType.CONNECTED:
                break

    def _create_process(self) -> PhoundPopen:
        cmd = [f"{Path(__file__).parent.resolve()}/bin/uccrobot", "-e", "-q"]

        _, log_file_dir = get_logging_parameters()
        if log_file_dir:
            cmd.extend(["-l", log_file_dir])
        cmd.append("-")

        # pylint: disable=W1509
        return cast(PhoundPopen, subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            # this is required in order not to receive parent's signals eg SIGINT
            preexec_fn=os.setpgrp,
            encoding="utf-8",
            bufsize=0
        ))

    def _destroy_process(self) -> None:
        self._process.stdin.close()
        self._process.stdout.close()
        self._process.wait()
        logger.info("UCC client process destroyed")

    def _write(self, cmd: str, log: bool = True) -> None:
        if log:
            logger.info(f"Sending cmd '{cmd}' to ucc")
        with lock:
            self._process.stdin.write(cmd + os.linesep)

    def _restart_not_running_process(self) -> None:
        while not self._health_check_thread.stopped():
            if self._process.poll() is not None:
                logger.error("Found UCC client process died, restarting")
                self._process = self._create_process()
                self._event_listener = EventListener(self._process.stdout)
                self._connect()
                if self._channels_enabled and self._channels_port:
                    self.enable_channels(self._channels_port)
            self._health_check_thread.wait(_HEALTH_CHECK_INTERVAL_SECONDS)


class _HealthCheckThread(threading.Thread):
    def __init__(self,  *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._event = threading.Event()

    def stop(self) -> None:
        self._event.set()

    def wait(self, timeout: int) -> None:
        self._event.wait(timeout)

    def stopped(self) -> bool:
        return self._event.is_set()
