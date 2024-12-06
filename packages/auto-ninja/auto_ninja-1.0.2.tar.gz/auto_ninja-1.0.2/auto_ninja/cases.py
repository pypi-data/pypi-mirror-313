import re


def kebab_case(text):
    return re.sub(r"([a-z])([A-Z])", r"\1-\2", text).lower()


def snake_case(text):
    return re.sub(r"([a-z])([A-Z])", r"\1_\2", text).lower()
