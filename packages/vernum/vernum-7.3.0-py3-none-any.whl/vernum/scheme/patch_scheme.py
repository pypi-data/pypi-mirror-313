from vernum.scheme import Scheme


class PatchScheme(Scheme):
    """Three part version numbers always with major, minor, and patch"""

    name = 'patch'

    FORMAT = r"^v?(\d+)\.(\d+)\.(\d+)$"

    INCREMENTS = ['major', 'minor', 'patch']

    # PATTERN = {
    #     'major': (+1, [0], [0]),
    #     'minor': (+0, +1, [0]),
    #     'patch': (+0, +0, +1)
    # }

    @classmethod
    def zero(cls):
        return cls(0, 0, 0)

    def __str__(self):
        if self.val:
            return '.'.join(str(i) for i in self.val)

    def increment(self, up: str):
        major, minor, patch = self.val
        if up == 'patch':
            patch += 1
        elif up == 'minor':
            minor += 1
            patch = 0
        elif up == 'major':
            major += 1
            minor = patch = 0
        return PatchScheme(major, minor, patch)
