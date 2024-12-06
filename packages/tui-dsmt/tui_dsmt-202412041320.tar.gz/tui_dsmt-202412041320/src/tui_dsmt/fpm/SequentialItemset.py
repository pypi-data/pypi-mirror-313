from typing import Callable, Any, Optional

from .Itemset import Itemset


class SequentialItemset(Itemset):
    def __new__(cls, *args, key: Callable[[str], Any] = None, reverse: bool = False):
        return super().__new__(cls, *args, modify=False)

    def __getitem__(self, key):
        if isinstance(key, slice):
            return SequentialItemset(*super().__getitem__(key))
        else:
            return super().__getitem__(key)

    def __add__(self, other):
        return SequentialItemset(*self, *other)

    def count_in(self, transactions):
        count = 0

        for _, transaction in transactions:
            for subset in transaction.subsets(len(self)):
                if subset == self:
                    count += 1
                    break

        return count

    def project(self, *prefix: str) -> Optional['SequentialItemset']:
        i = 0

        for k, e in enumerate(self, start=1):
            if e == prefix[i]:
                i += 1

            if i == len(prefix):
                return SequentialItemset(*self[k:])

    def __str__(self):
        return f'<{", ".join(map(str, self))}>'
