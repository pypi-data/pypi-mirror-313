from dataclasses import dataclass
import re

from vernum.scheme import Scheme


def prelabel(pre: int) -> str:
    return '-alpha' if pre == -2 else '-beta' if pre == -1 else ''


class PatchHyphenAlBeScheme(Scheme):
    """
    Example: 3.4.2-alpha
    """

    name = 'patch-hyphen-al-be'

    FORMAT = re.compile(
        r"^v?(\d+)\.(\d+)\.(\d+)(?:-(alpha|beta))?$")
    INCREMENTS = ['major', 'minor', 'patch', 'beta', 'alpha']

    @classmethod
    def parse(cls, string):
        """Because alpha and beta mean something, must use numbers"""
        if match := re.match(cls.FORMAT, string):
            major, minor, patch, prestr = match.groups()
            pre = -2 if prestr == 'alpha' else -1 if prestr == 'beta' else 0
            return cls(int(major), int(minor), int(patch), pre)

    def __str__(self):
        if self.val:
            major, minor, patch, pre = self.val
            result = f"{str(major)}.{str(minor)}.{str(patch)}"
            result += prelabel(pre)
            return result

    def increment(self, up: str):
        major, minor, patch, pre = self.val
        if up == 'alpha':
            return
        elif up == 'beta' and pre == -2:
            pre = -1
        elif up == 'patch':
            patch += 1
            pre = -2
        elif up == 'patch-zero':
            if pre == 0:
                patch += 1
            pre = 0
        elif up == 'minor':
            minor += 1
            patch = 0
            pre = -2
        elif up == 'minor-zero':
            if patch > 0 or pre == 0:
                minor += 1
            patch = pre = 0
        elif up == 'major':
            major += 1
            minor = patch = 0
            pre = -2
        elif up == 'major-zero':
            if minor > 0 or patch > 0 or pre == 0:
                major += 1
            minor = patch = pre = 0
        return PatchHyphenAlBeScheme(major, minor, patch, pre)
