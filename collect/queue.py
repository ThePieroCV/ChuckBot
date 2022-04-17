from collections import UserList
from random import sample


class ChuckQueue(UserList):
    def __init__(self, initlist) -> None:
        super().__init__(list(enumerate(initlist)))
        self.shuffled = False

    def next(self):
        self.data = self.data[1:]
        if not self.shuffled and self.data:
            self._reset_index()
        return self.data

    def extend(self, iterable):
        if self.data:
            indexes, _ = zip(*self.data)
        else:
            indexes = [-1]
        self.data = self.data + list(enumerate(iterable, max(indexes) + 1))
        if not self.shuffled:
            self._reset_index()
        return self.data

    def append(self, item):
        if self.data:
            indexes, _ = zip(*self.data)
        else:
            indexes = [-1]
        self.data = self.data + [(max(indexes) + 1, item)]
        if not self.shuffled:
            self._reset_index()
        return self.data

    def _reset_index(self):
        _, data = zip(*self.data)
        self.data = list(enumerate(data))
        return

    def rotate(self, cant=1):
        cant %= len(self.data)
        self.data = self.data[cant:] + self.data[:cant]
        if not self.shuffled:
            self._reset_index()
        return self.data

    def shuffle(self):
        if self.data:
            self.data = [self.data[0]] + sample(self.data[1:], len(self.data[1:]))
            self.shuffled = True
        return self.data

    def unshuffle(self):
        if self.data:
            idx = self.data[0][0]
            self.data.sort()
            _ = self.rotate(idx)
            self._reset_index()
            self.shuffled = False
        return self.data

    def __getitem__(self, idx: int):
        return self.data[idx][-1]
