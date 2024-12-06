import re

from wizlib.app import WizApp

from vernum.command import VerNumCommand

FORMAT = re.compile(r"^v?(\d+)\.(\d+)\.(?:(\d+)|beta(\d+)|alpha(\d+))$")


class VerNumApp(WizApp):

    base_command = VerNumCommand
    name = 'vernum'


# def string2val(string):
#     """Convert a string like "1.2.3" to a tuple i.e. (1,2,3)"""
#     if match := FORMAT.match(string):
#         return tuple((-1 if (x is None) else int(x)) for x in match.groups())


# def val2string(major, minor, patch, beta, alpha):
#     """Convert a value list (1,2,3) to a string like "1.2.3" """
#     if alpha >= 0:
#         final = f'alpha{alpha}'
#     elif beta >= 0:
#         final = f'beta{beta}'
#     elif patch >= 0:
#         final = str(patch)
#     return f"{major}.{minor}.{final}"
