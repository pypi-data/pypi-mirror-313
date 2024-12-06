from typing import Callable, Dict, List

class EventManagerError(Exception):
    """Base class for Event Manager exceptions."""
    pass

class EventAlreadyRegistered(EventManagerError):
    """Raised when an event is already registered."""
    pass

class EventNotRegistered(EventManagerError):
    """Raised when an event is not registered."""
    pass

class CallbackAlreadySubscribed(EventManagerError):
    """Raised when a callback is already subscribed to an event."""
    pass

class CallbackNotSubscribed(EventManagerError):
    """Raised when a callback is not subscribed to an event."""
    pass