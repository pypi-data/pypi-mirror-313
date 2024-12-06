from typing import Callable, Dict, List
from Events.exceptions import (
    EventNotRegistered, EventManagerError, CallbackNotSubscribed,
    EventAlreadyRegistered, CallbackAlreadySubscribed
)

class EventManager:
    """
    A class for managing events and their associated callbacks.

    This class allows for event registration, callback subscription, and event
    notification, supporting a simple publish-subscribe mechanism.

    Attributes:
        _events (Dict[str, List[Callable]]): A dictionary where keys are event 
        names and values are lists of callback functions subscribed to each event.

    Methods:
        register_event(event_name: str): Registers a new event.
        deregister_event(event_name: str): Removes an event and its subscribers.
        subscribe(event_name: str, callback: Callable): Subscribes a callback to an event.
        unsubscribe(event_name: str, callback: Callable): Removes a callback from an event.
        call_event(event_name: str, *args, **kwargs): Calls an event, notifying callbacks.
        event(event_name: str): A decorator for subscribing functions to an event.
    """

    def __init__(self):
        """Initialize the EventManager with an empty event registry."""
        self._events: Dict[str, List[Callable]] = {}

    def register_event(self, event_name: str) -> None:
        """
        Register a new event by name.

        Args:
            event_name (str): The name of the event to register.

        Raises:
            EventAlreadyRegistered: If the event is already registered.
        """
        if event_name in self._events:
            raise EventAlreadyRegistered(f"Event '{event_name}' is already registered.")
        self._events[event_name] = []

    def deregister_event(self, event_name: str) -> None:
        """
        Deregister an event, removing it and all its associated callbacks.

        Args:
            event_name (str): The name of the event to deregister.

        Raises:
            EventNotRegistered: If the event is not registered.
        """
        if event_name not in self._events:
            raise EventNotRegistered(f"Event '{event_name}' is not registered.")
        del self._events[event_name]

    def subscribe(self, event_name: str, callback: Callable) -> None:
        """
        Subscribe a callback function to an event.

        Args:
            event_name (str): The name of the event.
            callback (Callable): The callback function to subscribe.

        Raises:
            EventNotRegistered: If the event is not registered.
            CallbackAlreadySubscribed: If the callback is already subscribed to the event.
        """
        if event_name not in self._events:
            raise EventNotRegistered(f"Event '{event_name}' is not registered.")
        if callback in self._events[event_name]:
            raise CallbackAlreadySubscribed(
                f"Callback '{callback.__name__}' is already subscribed to event '{event_name}'."
            )
        self._events[event_name].append(callback)

    def unsubscribe(self, event_name: str, callback: Callable) -> None:
        """
        Unsubscribe a callback function from an event.

        Args:
            event_name (str): The name of the event.
            callback (Callable): The callback function to unsubscribe.

        Raises:
            EventNotRegistered: If the event is not registered.
            CallbackNotSubscribed: If the callback is not subscribed to the event.
        """
        if event_name not in self._events:
            raise EventNotRegistered(f"Event '{event_name}' is not registered.")
        try:
            self._events[event_name].remove(callback)
        except ValueError:
            raise CallbackNotSubscribed(
                f"Callback '{callback.__name__}' is not subscribed to event '{event_name}'."
            )

    def call_event(self, event_name: str, *args, **kwargs) -> None:
        """
        Call an event, notifying all subscribed callbacks.

        Args:
            event_name (str): The name of the event.
            *args: Positional arguments to pass to the callbacks.
            **kwargs: Keyword arguments to pass to the callbacks.

        Raises:
            EventNotRegistered: If the event is not registered.
        """
        if event_name not in self._events:
            raise EventNotRegistered(f"Event '{event_name}' is not registered.")
        for callback in self._events[event_name]:
            try:
                callback(*args, **kwargs)
            except Exception as e:
                raise EventManagerError(
                    f"Error occurred while executing callback '{callback.__name__}' for event '{event_name}': {e}"
                )

    def event(self, event_name: str):
        """
        Decorator to subscribe a function to an event.

        Args:
            event_name (str): The name of the event.

        Returns:
            Callable: A decorator function to subscribe the decorated function.

        Example:
            @event_manager.event("greet")
            def greet_handler(name):
                print(f"Greetings, {name}!")
        """
        def decorator_function(callback: Callable):
            self.subscribe(event_name, callback)
            return callback  # Return the original function for normal use
        return decorator_function
