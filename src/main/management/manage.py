import sys
from main.management.commands import startapp
from main.management import std, exc

command_handlers = {
    "startapp": startapp.StartAppCommand(),
    "do_something": "",
}

this_path, command, *command_args = sys.argv

handler = command_handlers.get(command)
if not handler:
    std.print_error(
        (
            "No handler found for command '{command}'"
            " Avaialable commands:\n * {commands}"
        ).format(command=command, commands="\n * ".join(command_handlers.keys()))
    )

    std.print_error("\nExiting\n")
    exit()

try:
    handler.handle(command_args)
except exc.CommandError as e:
    std.print_error(e.args[0])
    std.print_error("\nExiting\n")
    exit()

handler.execute()
