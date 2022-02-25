import logging
from typing import Callable, Dict, List, Union, Type

from main.domain import command, event


Message = Union[command.Command, event.Event]
CommandHandlerDict = Dict[Type[command.Command], Callable]
EventHandlerDict = Dict[Type[event.Event], List[Callable]]
logger = logging.getLogger("bus")


class MessageBus:

    command_handlers: CommandHandlerDict
    event_handlers: EventHandlerDict

    def __init__(
        self,
        command_handlers: CommandHandlerDict,
        event_handlers: EventHandlerDict,
    ):
        self.command_handlers = command_handlers
        self.event_handlers = event_handlers

    async def _handle_command(self, command: command.Command):
        handler = None
        try:
            handler = self.command_handlers[type(command)]
            return await handler(command)
        except Exception:
            logger.exception(f"Failed to handle {command=} using {handler=}")
            raise

    async def _handle_event(self, event: event.Event):
        handler = None
        events = []
        try:
            handlers = self.event_handlers[type(event)]
            for handler in handlers:
                new_events = await handler(event)
                if new_events:
                    events.append(new_events)
        except Exception:
            logger.exception(f"Failed to handle {event=} using {handler=}")
            raise
        return events

    async def handle(self, message: Message):

        self.queue = [message]
        while self.queue:
            message = self.queue.pop(0)
            if isinstance(message, command.Command):
                new_events = await self._handle_command(message)
            elif isinstance(message, event.Event):
                new_events = await self._handle_event(message)
            else:
                raise ValueError(
                    f"{message=} is not an {command.Command} or {event.Event}"
                )
            if new_events:
                self.queue.extend(new_events)
