# from dataclasses import dataclass
import re

from wizlib.class_family import ClassFamily


# def notch(value, up):
#     if type(up) == list:
#         return up[0]
#     else:
#         return value + up


# @dataclass
class Scheme(ClassFamily):
    """Represents a version numbering scheme or system."""

    val: tuple

    def __init__(self, *val):
        """val is a tuple that defines ordering"""
        self.val = val

    def __str__(self):
        """Default string rendering assumes just numbers"""
        if self.val:
            return '.'.join(str(i) for i in self.val)

    @classmethod
    def parse(cls, string):
        """Return an instance by parsing a string"""
        if match := re.match(cls.FORMAT, string):
            groups = match.groups()
            return cls(*tuple(neg4none(x) for x in groups))


def neg4none(value):
    return -1 if (value is None) else int(value)
