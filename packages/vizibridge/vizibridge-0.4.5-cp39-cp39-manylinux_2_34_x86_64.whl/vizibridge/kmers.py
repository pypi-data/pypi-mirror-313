import vizibridge._vizibridge as rust_types
from typing import Self

Pykmers = [
    getattr(rust_types, a)
    for a in dir(rust_types)
    if a.startswith("PyKmer") or a.startswith("PyLongKmer")
]

KmerType = Pykmers[0]
for t in Pykmers[1:]:
    KmerType |= t

KmerTypeMap = {KT.size(): KT for KT in Pykmers}


class Kmer:
    __slots__ = ("__data",)

    def __init__(self, data: KmerType | int, size: int | None = None):
        if isinstance(data, int):
            assert size
            data = KmerTypeMap[size](data)
        self.__data = data

    def __getstate__(self):
        return dict(base_cls=type(self.__data).size(), data=self.__data.data)

    def __setstate__(self, state):
        self.__data = KmerTypeMap[state["base_cls"]](state["data"])

    @classmethod
    def from_dna(cls, seq) -> Self:
        return list(seq.enum_kmer(len(seq)))[0]

    @property
    def size(self) -> int:
        return type(self.__data).size()

    @property
    def data(self) -> int:
        return self.__data.data

    @property
    def base_type(self) -> KmerType:
        return self.__data

    def __repr__(self):
        return repr(self.__data)

    def __str__(self):
        return str(self.__data)

    def __hash__(self):
        return hash(self.__data)

    def add_left_nucleotid(self, c: str) -> Self:
        return type(self)(self.__data.add_left_nucleotid(c))

    def add_right_nucleotid(self, c: str) -> Self:
        return type(self)(self.__data.add_right_nucleotid(c))

    def reverse_complement(self) -> Self:
        return type(self)(self.__data.reverse_complement())

    def is_canonical(self) -> bool:
        return self.__data.is_canonical()

    def canonical(self) -> Self:
        return type(self)(self.__data.canonical())

    def __lt__(self, other) -> bool:
        return self.__data < other.__data

    def __gt__(self, other) -> bool:
        return self.__data < other.__data

    def __eq__(self, other) -> bool:
        return (
            type(self) is type(other)
            and self.size == other.size
            and self.data == other.data
        )
