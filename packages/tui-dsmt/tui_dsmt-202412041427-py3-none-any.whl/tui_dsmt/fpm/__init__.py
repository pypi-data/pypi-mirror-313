from .BruteForceFI import BruteForceFI
from .FPTree import FPTree
from .HashTree import HashTree
from .Itemset import Itemset
from .ItemsetGrid import ItemsetGrid
from .ItemsetGridApriori import ItemsetGridApriori
from .ItemsetGridECLAT import ItemsetGridECLAT
from .SequentialDatabase import SequentialDatabase
from .SequentialItemset import SequentialItemset
from .TransactionDatabase import TransactionDatabase

receipts = TransactionDatabase(
    (1, Itemset('Brot', 'Milch')),
    (2, Itemset('Butter', 'Mehl')),
    (3, Itemset('Brot', 'Butter', 'Eier')),
    (4, Itemset('Brot', 'Milch', 'Eier')),
    (5, Itemset('Butter', 'Eier')),
)

receipts1 = TransactionDatabase(
    (1, Itemset('Brot', 'Butter', 'Milch', 'Zucker')),
    (2, Itemset('Butter', 'Mehl', 'Milch', 'Zucker')),
    (3, Itemset('Butter', 'Eier', 'Milch', 'Salz')),
    (4, Itemset('Eier')),
    (5, Itemset('Butter', 'Mehl', 'Milch', 'Salz', 'Zucker')),
)

sequential_receipts = SequentialDatabase(
    (1, SequentialItemset('Eier', 'Brot', 'Milch', 'Käse')),
    (2, SequentialItemset('Milch', 'Eier', 'Butter')),
    (3, SequentialItemset('Brot', 'Butter', 'Eier')),
    (4, SequentialItemset('Brot', 'Milch', 'Käse')),
    (5, SequentialItemset('Brot', 'Eier', 'Milch')),
    (6, SequentialItemset('Brot', 'Eier'))
    # (1, SequentialItemset('Brot', 'Milch', 'Eier')),
    # (2, SequentialItemset('Milch', 'Eier')),
    # (3, SequentialItemset('Brot', 'Butter', 'Eier')),
    # (4, SequentialItemset('Brot', 'Milch'))
)

numbers = TransactionDatabase(
    (100, Itemset(1, 3, 4)),
    (200, Itemset(2, 3, 5)),
    (300, Itemset(1, 2, 3, 5)),
    (400, Itemset(2, 5)),
)

extended_numbers = TransactionDatabase(
    (100, Itemset(1, 3, 4)),
    (200, Itemset(2, 3, 5)),
    (300, Itemset(1, 2, 3, 5)),
    (400, Itemset(2, 5)),
    (500, Itemset(1, 2, 3)),
    (600, Itemset(1, 2, 4)),
    (700, Itemset(1, 2, 4)),
)

characters = TransactionDatabase(
    (100, Itemset('f', 'a', 'c', 'd', 'g', 'i', 'm', 'p')),
    (200, Itemset('a', 'b', 'c', 'f', 'l', 'm', 'o')),
    (300, Itemset('b', 'f', 'm', 'h', 'j', 'o')),
    (400, Itemset('b', 'c', 'k', 's', 'p')),
    (500, Itemset('a', 'f', 'c', 'e', 'l', 'p', 'm', 'n')),
    (600, Itemset('f', 'c', 'p', 'n')),
)

characters2 = TransactionDatabase(
    (100, Itemset('f', 'a', 'c', 'd', 'g', 'i', 'm', 'p')),
    (200, Itemset('a', 'b', 'c', 'f', 'l', 'm', 'o')),
    (300, Itemset('b', 'f', 'h', 'j', 'o')),
    (400, Itemset('b', 'c', 'k', 's', 'p')),
    (500, Itemset('a', 'f', 'c', 'e', 'l', 'p', 'm', 'n')),
)

dna = SequentialDatabase(
    (1, SequentialItemset(*'AGAAGT')),
    (2, SequentialItemset(*'TGACAG')),
    (3, SequentialItemset(*'GAAGT'))
)
