from dataclasses import dataclass
from argparse import ArgumentParser
import os

from wizlib.command import WizCommand
from wizlib.input_handler import InputHandler
from wizlib.config_handler import ConfigHandler

from vernum.scheme import Scheme
from vernum.error import VerNumError


class VerNumCommand(WizCommand):

    default = 'full'
    handlers = [InputHandler, ConfigHandler]

    @property
    def scheme(self):
        name = self.config.get('vernum-scheme') or 'patch'
        scheme = Scheme.family_member('name', name)
        if not scheme:
            raise VerNumError(f"Invalid scheme '{name}'")
        return scheme
