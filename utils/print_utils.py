from termcolor import cprint


def print_success(message):
    cprint(message, "green", "on_black")


def print_error(message):
    cprint(message, "red", "on_black")


def print_neutral(message):
    cprint(message, "light_grey", "on_black")
