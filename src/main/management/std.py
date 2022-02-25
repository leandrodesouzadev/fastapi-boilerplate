from colorama import init, Fore

init()


def print_error(message: str):
    print(Fore.RED + message)


def print_sucess(message: str):
    print(Fore.GREEN + message)
