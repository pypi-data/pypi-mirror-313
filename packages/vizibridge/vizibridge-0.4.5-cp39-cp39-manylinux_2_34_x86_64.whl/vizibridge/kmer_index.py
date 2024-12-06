import vizibridge._vizibridge as rust_types
from vizibridge.kmers import Kmer, KmerType
from vizibridge.DNA import DNA, rust_DNA
from vizibridge.kmer_set import KmerSet
from typing import Self, Iterator
from collections.abc import Mapping
from pathlib import Path
from dataclasses import dataclass

from typing import Set, Mapping

@dataclass
class KmerIndexEntry:
    kmer: KmerType | Kmer
    val: int


@dataclass
class DNAIndexEntry:
    DNA: DNA | rust_DNA
    val: int


kmer_indexes = [
    getattr(rust_types, a)
    for a in dir(rust_types)
    if a.startswith("KmerIndex") or a.startswith("LongKmerIndex")
]

KmerIndexType = kmer_indexes[0]
for t in kmer_indexes[1:]:
    KmerIndexType |= t

KmerIndexTypeMap = {KT.size(): KT for KT in kmer_indexes}


class KmerIndex(Mapping):
    __slots__ = ("__base_index", "__k")

    def __init__(self, path: Path, k: int):
        if not path.exists():
            raise IOError(path)
        self.__base_index = KmerIndexTypeMap[k](str(path))
        self.__k = k

    @property
    def k(self):
        return self.__k

    @property
    def base_index(self):
        return self.__base_index

    def __getitem__(self, kmer: KmerType | Kmer):
        if isinstance(kmer, KmerType):
            return self.__base_index[kmer]
        return self.__base_index[kmer.base_type]

    def __len__(self):
        return len(self.__base_index)

    def items_iter(self):
        return iter(self.__base_index)

    def __iter__(self):
        yield from (index_entry.kmer for index_entry in self.items_iter())

    @classmethod
    def build(
        cls,
        iterator: Iterator[KmerIndexEntry],
        index_path: Path,
        k: int,
        buffer_size=10**7,
    ) -> Self:
        BaseIndexType = KmerIndexTypeMap[k]
        if index_path.exists():
            raise IOError("path already exists")
        iterator = map(
            lambda e: KmerIndexEntry(
                kmer=getattr(e.kmer, "base_type", e.kmer), val=e.val
            ),
            iterator,
        )
        BaseIndexType.build(iterator, str(index_path), buffer_size=buffer_size)
        return cls(index_path, k)

    @classmethod
    def build_dna(
        cls,
        iterator: Iterator[DNAIndexEntry],
        index_path: Path,
        k: int,
        index: int,
        modulo: int,
        buffer_size=10**7,
    ) -> Self:
        BaseIndexType = KmerIndexTypeMap[k]
        if index_path.exists():
            raise IOError("path already exists")
        iterator = map(
            lambda e: DNAIndexEntry(DNA=getattr(e.DNA, "data", e.DNA), val=e.val),
            iterator,
        )
        BaseIndexType.build_dna(
            iterator,
            str(index_path),
            buffer_size=buffer_size,
            index=index,
            modulo=modulo,
        )
        return cls(index_path, k)

    def join(
        self,
        iterator: Iterator[KmerIndexEntry],
        out_path: Path,
        buffer_size=10**7
    ) -> Mapping[int, int]:
        if out_path.exists():
            raise IOError("path already exists")
        return self.base_index.join_iter32(iterator, str(out_path), buffer_size) 

    def intersection(
        self,
        iterator: Iterator[Kmer],
        out_path: Path,
        buffer_size=10**7
    ) -> Set[int]:
        if out_path.exists():
            raise IOError("path already exists")
        return self.base_index.intersection_iter32(iterator, str(out_path), buffer_size) 

    def intersection_index(
        self,
        other: KmerSet,
        out_path: Path,
        buffer_size=10**7
    ) -> Mapping[int, int]:
        if out_path.exists():
            raise IOError("path already exists")
        return self.base_index.intersection_index(other.base_index, str(out_path), buffer_size) 

    def join_index(
        self,
        other: Self,
        out_path: Path,
        buffer_size=10**7
    ) -> Mapping[int, int]:
        if out_path.exists():
            raise IOError("path already exists")
        return self.base_index.join_index(other.base_index, str(out_path), buffer_size) 

