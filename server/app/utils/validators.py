import re

MOBILE_PATTERN = re.compile(r"^\d{10}$")
EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def is_valid_email(value: str) -> bool:
    return bool(EMAIL_PATTERN.fullmatch(value.strip()))


def is_valid_mobile_number(value: str) -> bool:
    return bool(MOBILE_PATTERN.fullmatch(value.strip()))
