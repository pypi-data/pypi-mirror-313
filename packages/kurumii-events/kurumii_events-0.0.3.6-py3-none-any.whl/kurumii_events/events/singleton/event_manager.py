from typing import Callable, Dict, List
from kurumii_events.events.exceptions import (
    EventNotRegistered, EventManagerError, CallbackNotSubscribed,
    EventAlreadyRegistered, CallbackAlreadySubscribed
)

class EventManager:
    """
    A singleton class for managing events and their associated callbacks.
    """
    _instance = None
    _events: Dict[str, List[Callable]] = {}

    def __new__(cls):
        """Ensure only one instance of EventManager is created."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def register_event(self, event_name: str) -> None:
        """Register a new event by name."""
        if event_name in self._events:
            raise EventAlreadyRegistered(f"Event '{event_name}' is already registered.")
        self._events[event_name] = []

    def deregister_event(self, event_name: str) -> None:
        """Deregister an event."""
        if event_name not in self._events:
            raise EventNotRegistered(f"Event '{event_name}' is not registered.")
        del self._events[event_name]

    def subscribe(self, event_name: str, callback: Callable) -> None:
        """Subscribe a callback function to an event."""
        if event_name not in self._events:
            raise EventNotRegistered(f"Event '{event_name}' is not registered.")
        if callback in self._events[event_name]:
            raise CallbackAlreadySubscribed(f"Callback '{callback.__name__}' is already subscribed.")
        self._events[event_name].append(callback)

    def unsubscribe(self, event_name: str, callback: Callable) -> None:
        """Unsubscribe a callback function from an event."""
        if event_name not in self._events:
            raise EventNotRegistered(f"Event '{event_name}' is not registered.")
        try:
            self._events[event_name].remove(callback)
        except ValueError:
            raise CallbackNotSubscribed(f"Callback '{callback.__name__}' is not subscribed.")

    def call_event(self, event_name: str, *args, **kwargs) -> None:
        """Call an event, notifying all subscribed callbacks."""
        if event_name not in self._events:
            raise EventNotRegistered(f"Event '{event_name}' is not registered.")
        for callback in self._events[event_name]:
            try:
                callback(*args, **kwargs)
            except Exception as e:
                raise EventManagerError(f"Error while executing callback '{callback.__name__}' for event '{event_name}': {e}")

    def event(self, event_name: str):
        """Decorator to subscribe a function to an event."""
        def decorator_function(callback: Callable):
            self.subscribe(event_name, callback)
            return callback  # Return the original function for normal use
        return decorator_function
