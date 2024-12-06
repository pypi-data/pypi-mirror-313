from typing import Tuple, List, Set

from .SequentialItemset import SequentialItemset


class SequentialDatabase(List[Tuple[int, Tuple[SequentialItemset, ...]]]):
    def __init__(self, *args: Tuple[int, SequentialItemset]):
        super().__init__(args)

    def project(self, *prefix: str) -> 'SequentialDatabase':
        return SequentialDatabase(*filter(
            lambda x: x[1] is not None,
            (
                (tid, transaction.project(*prefix))
                for tid, transaction in self
            )
        ))

    @property
    def items(self) -> Set[SequentialItemset]:
        return set(
            SequentialItemset(x)
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
    def item_powerset(self) -> 'SequentialDatabase':
        items = list(self.items)

        def generate(l: int):
            if l == 0:
                return

            for i in items:
                yield i
                for k in generate(l - 1):
                    if i[0] not in k:
                        yield i + k

        return SequentialDatabase(*enumerate(sorted(generate(self.max_length))))
