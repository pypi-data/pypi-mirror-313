from typing import TextIO

from phound import events
from phound.events import EventType, Event
from phound import exceptions


class EventListener:
    def __init__(self, source: TextIO) -> None:
        self._source = source

    def wait_event(self, *event_types: EventType) -> Event:
        while True:
            event = self._get_next_event()
            self._raise_for_error(event)
            if not self._should_ignore_event(event):
                break
        if event_types and event.type not in event_types:
            raise exceptions.UnexpectedEventError(
                f"Unexpected event: {event.type}, expected: {', '.join(event_types)}")
        return event

    def _get_next_event(self) -> Event:
        while True:
            data = self._source.readline()
            if not data:
                raise exceptions.InputError
            event = events.parse(data)
            if event:
                return event

    def _should_ignore_event(self, event: Event) -> bool:
        return event.type in (EventType.CHAT_MESSAGE_OBJECT_ID,)

    @staticmethod
    def _raise_for_error(event: Event) -> None:
        if event.type == EventType.ERROR:
            raise exceptions.PhoundError(event.body)
        if event.type == EventType.CHAT_ERROR:
            raise exceptions.ChatError(event.body)
