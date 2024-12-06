import itertools
from typing import Callable, Any


class Itemset(tuple):
    def __new__(cls, *args, key: Callable[[str], Any] = None, reverse: bool = False, modify: bool = True):
        if modify:
            return super().__new__(cls, sorted(set(args), key=key, reverse=reverse))
        else:
            return super().__new__(cls, args)

    def __getitem__(self, key):
        if isinstance(key, slice):
            return Itemset(*super().__getitem__(key), modify=False)
        else:
            return super().__getitem__(key)

    @property
    def set(self):
        return set(self)

    def is_subset(self, transaction):
        return self.set.issubset(transaction)

    def count_in(self, transactions):
        c = 0
        for _, items in transactions:
            if self.is_subset(items):
                c += 1

        return c

    def support_in(self, transactions):
        return self.count_in(transactions) / len(transactions)

    def matches(self, other, length):
        return self[:length] == other[:length] and self[length:] != other[length:]

    def union(self, other):
        return Itemset(*self, *other)

    def subsets(self, length):
        yield from itertools.combinations(self, length)

    def sort(self, key: Callable[[str], Any] = None, reverse: bool = False):
        return Itemset(*self, key=key, reverse=reverse)

    def filter(self, key: Callable[[str], bool]):
        return Itemset(*filter(key, self))
