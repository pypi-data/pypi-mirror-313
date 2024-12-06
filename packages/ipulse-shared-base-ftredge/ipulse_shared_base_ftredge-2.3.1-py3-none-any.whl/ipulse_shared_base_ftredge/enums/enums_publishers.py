# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
from enum import Enum


class PublisherStatus(Enum):
    OPEN = "open"
    CLOSED = "closed"
    CANCELLED = "cancelled"
    MAINTENANCE = "maintenance"
    BREAK="break"
    HOLIDAY="holiday"
    UNREACHABLE = "unreachable"
    PERMANENTLY_CLOSED="permanently_closed"

    def __str__(self):
        return self.value