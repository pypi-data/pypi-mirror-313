from dataclasses import dataclass
import re

from vernum.scheme import Scheme


class MinorAlphaBetaScheme(Scheme):
    """
    Supports alpha and beta prepatch versions, applied at the minor level.

    Example: 3.4.alpha2
    """

    name = 'minor-alpha-beta'

    FORMAT = re.compile(
        r"^v?(\d+)\.(\d+)\.(?:(\d+)|beta(\d+)|alpha(\d+))$")
    INCREMENTS = ['major', 'minor', 'patch', 'beta', 'alpha']

    def __str__(self):
        if self.val:
            r = f"{str(self.val[0])}.{str(self.val[1])}."
            if self.val[4] > -1:
                return r + f"alpha{str(self.val[4])}"
            if self.val[3] > -1:
                return r + f"beta{str(self.val[3])}"
            return r + str(self.val[2])

    def increment(self, up: str):
        major, minor, patch, beta, alpha = self.val
        if up == 'alpha':
            if alpha + 1:
                alpha += 1
            elif beta + 1:
                beta += 1
            else:
                return
        elif up == 'beta':
            if beta + 1:
                beta += 1
            elif alpha + 1:
                beta = 1
                alpha = -1
            else:
                return
        elif up == 'patch':
            if patch + 1:
                patch += 1
            elif beta + 1 or alpha + 1:
                patch = 0
                beta = alpha = -1
            else:
                return
        elif up == 'minor':
            minor += 1
            alpha = 1
            patch = beta = -1
        elif up == 'minor-zero':
            minor += 1
            patch = 0
            beta = alpha = -1
        elif up == 'major':
            major += 1
            minor = 0
            alpha = 1
            patch = beta = -1
        elif up == 'major-zero':
            major += 1
            minor = patch = 0
            beta = alpha = -1
        return MinorAlphaBetaScheme(major, minor, patch, beta, alpha)
