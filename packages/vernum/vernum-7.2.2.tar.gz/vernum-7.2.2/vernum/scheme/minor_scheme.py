from vernum.scheme import Scheme


class MinorScheme(Scheme):
    """Two part version numbers always with major and minor"""

    name = 'minor'

    FORMAT = r"^v?(\d+)\.(\d+)$"
    INCREMENTS = ['major', 'minor']

    @classmethod
    def zero(cls):
        return cls(0, 0)

    def increment(self, up: str):
        major, minor = self.val
        if up == 'minor':
            minor += 1
        elif up == 'major':
            major += 1
            minor = 0
        return MinorScheme(major, minor)
