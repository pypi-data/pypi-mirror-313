from vernum.scheme import Scheme


class MajorScheme(Scheme):
    """Just a number"""

    name = 'major'

    FORMAT = r"^v?(\d+)$"
    INCREMENTS = ['major']

    def increment(self, up: str = 'major'):
        major, = self.val
        if up == 'major':
            major += 1
        return MajorScheme(major,)
