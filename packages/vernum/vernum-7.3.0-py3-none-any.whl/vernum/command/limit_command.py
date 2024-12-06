from argparse import ArgumentParser
from getpass import getpass
from functools import reduce
import sys

from vernum.command import VerNumCommand
from vernum.error import VerNumError
from vernum.scheme import Scheme


class LimitCommand(VerNumCommand):
    """Limit a version number to a minimum"""

    name = 'limit'

    @VerNumCommand.wrap
    def execute(self):
        """Limit a version number to a minimum"""
        limit_str = self.config.get('vernum-limit-min')
        limit = self.scheme.parse(limit_str)
        vernum_str = self.input.text
        vernum = self.scheme.parse(vernum_str)
        if (vernum is None):
            raise VerNumError(f"Invalid version number {vernum_str}")
        if vernum.val < limit.val:
            raise VerNumError(f"Limit violation: {vernum_str} < {limit_str}")
        self.status = f"{vernum_str} >= {limit_str}"

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
