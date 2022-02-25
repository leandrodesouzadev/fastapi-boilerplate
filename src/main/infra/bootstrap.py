import inspect
from typing import Dict, Any, Callable

from . import bus
from auth.services import handlers


def bootstrap_message_bus() -> bus.MessageBus:
    dependencies: Dict[str, Any] = {}

    injected_event_handlers = {
        event_type: [
            inject_dependencies(handler, dependencies) for handler in event_handlers
        ]
        for event_type, event_handlers in handlers.EVENT_HANDLERS.items()
    }
    injected_command_handlers = {
        command_type: inject_dependencies(handler, dependencies)
        for command_type, handler in handlers.COMMAND_HANDLERS.items()
    }
    return bus.MessageBus(injected_command_handlers, injected_event_handlers)


def inject_dependencies(handler: Callable, dependencies: Dict[str, Any]):
    params = inspect.signature(handler).parameters
    deps = {
        name: dependency for name, dependency in dependencies.items() if name in params
    }
    return lambda message: handler(message, **deps)
