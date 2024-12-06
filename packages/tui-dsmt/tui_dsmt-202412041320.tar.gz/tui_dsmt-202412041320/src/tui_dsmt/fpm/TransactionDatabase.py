import itertools
from typing import Tuple, List, Set

from .Itemset import Itemset


class TransactionDatabase(List[Tuple[int, Tuple[Itemset, ...]]]):
    def __init__(self, *args: Tuple[int, Itemset]):
        super().__init__(args)

    @property
    def items(self) -> Set[Itemset]:
        return set(
            Itemset(x)
            for _, transaction in self
            for x in transaction
        )

    @property
    def max_length(self) -> int:
        return max(
            len(transaction)
            for _, transaction in self
        )

    @property
    def powerset(self) -> 'TransactionDatabase':
        s = [x[0] for x in self.items]

        return TransactionDatabase(
            *enumerate(
                sorted(
                    map(
                        lambda x: Itemset(*x),
                        filter(
                            len,
                            itertools.chain.from_iterable(
                                itertools.combinations(s, r)
                                for r in range(len(s) + 1)
                            )
                        )
                    )
                )
            )
        )
