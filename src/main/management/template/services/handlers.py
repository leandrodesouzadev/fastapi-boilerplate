from typing import Dict, List, Callable, Type
from main.domain import command, event


# Create your handlers here


COMMAND_HANDLERS: Dict[Type[command.Command], Callable] = {}

EVENT_HANDLERS: Dict[Type[event.Event], List[Callable]] = {}
