from dataclasses import dataclass
from getpass import getpass
from functools import reduce
import sys

from wizlib.parser import WizParser
from vernum.error import VerNumError

from vernum.command import VerNumCommand
from vernum.scheme import Scheme


class NextCommand(VerNumCommand):
    """Increment the version"""

    name = 'next'

    @classmethod
    def add_args(cls, parser: WizParser):
        super().add_args(parser)
        parser.add_argument('increment')

    @VerNumCommand.wrap
    def execute(self):
        if not hasattr(self, 'increment'):
            raise VerNumError(f"VerNum 'next' command requires an increment")
        if self.increment not in self.scheme.INCREMENTS:
            raise VerNumError(f"Invalid increment '{self.increment}' " +
                              "for scheme '{self.scheme.name}'")
        current = self.scheme.parse(self.stripped)
        if current:
            next = current.increment(self.increment)
            if not next:
                raise VerNumError(f"Invalid increment '{self.increment} " +
                                  f"for version '{current}'")
            self.status = f"Version number incremented " + \
                f"from {current} to {next}"
            return str(next)
        else:
            raise VerNumError(f"Invalid version string '{self.stripped}' " +
                              f"for scheme '{self.scheme.name}'")

    @property
    def stripped(self):
        return self.input.text.strip()
