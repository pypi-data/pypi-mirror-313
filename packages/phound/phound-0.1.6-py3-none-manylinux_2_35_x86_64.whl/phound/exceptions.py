class PhoundError(Exception):
    pass


class EventParseError(PhoundError):
    pass


class UnexpectedEventError(PhoundError):
    pass


class ChatError(PhoundError):
    pass


class InputError(PhoundError):
    pass
