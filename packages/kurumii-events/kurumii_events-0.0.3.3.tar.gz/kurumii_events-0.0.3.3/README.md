# Installation:

```bash
pip install kurumii_events
```

# Usage

```python
from kurumii_events import EventManager
# Create an EventManager instance
manager = EventManager()

# Register an event
manager.register_event("greet")

# Define a callback
def say_hello(name):
    print(f"Hello, {name}!")

# Subscribe the callback to the event
manager.subscribe("greet", say_hello)

# Emit the event
manager.emit("greet", name="Alice")  # Output: "Hello, Alice!"

# Unsubscribe the callback
manager.unsubscribe("greet", say_hello)

# Decorator usage
@manager.event("greet")
def another_greeting(name):
    print(f"Hi, {name}!")

# Emit the event again
manager.emit("greet", name="Bob")  # Output: "Hi, Bob!"

```