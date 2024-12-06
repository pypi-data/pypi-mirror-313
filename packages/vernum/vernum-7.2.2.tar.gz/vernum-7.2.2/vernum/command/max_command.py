from argparse import ArgumentParser
from getpass import getpass
from functools import reduce
import sys

from vernum.command import VerNumCommand
from vernum.scheme import Scheme


class MaxCommand(VerNumCommand):
    """Return the highest of a set of version strings"""

    name = 'max'

    @VerNumCommand.wrap
    def execute(self):
        """Return the highest of a set of version numbers"""
        verstringlist = self.input.text.split('\n')
        vernums = [v for s in verstringlist if (v := self.scheme.parse(s))]
        if vernums:
            maxval = max(vernums, key=lambda v: v.val)
            self.status = f"Found max version number {maxval}"
            return str(maxval)
        else:
            self.status = f"Version list is empty"

        # current = scheme.parse(self.input)
        # next = getattr(current.increment, self.increment)
        # self.status = f'Version number incremented from {current} to {next}'
        # return str(next)

        # zeroval = (0, 0, 0, -1, -1)
        # verstringlist = self.input.split('\n')
        # vals = [v for s in verstringlist if (v := string2val(s))]
        # maxval = reduce(max, vals, zeroval)
        # self.status = 'Done'
        # return val2string(*maxval)
