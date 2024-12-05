import vizibridge._vizibridge as rust_types
from vizibridge.kmers import Kmer, KmerType
from vizibridge.DNA import DNA, rust_DNA
from typing import Self, Iterator
from collections.abc import Set
from pathlib import Path
from dataclasses import dataclass

# KmerSet definitions

kmer_set = [
    getattr(rust_types, a)
    for a in dir(rust_types)
    if a.startswith("KmerSet") or a.startswith("LongKmerSet")
]

KmerSetType = kmer_set[0]
for t in kmer_set[1:]:
    KmerSetType |= t

KmerSetTypeMap = {KT.size(): KT for KT in kmer_set}


class KmerSet(Set):
    __slots__ = ("__base_index", "__k")

    def __init__(self, path: Path, k: int):
        if not path.exists():
            raise IOError(path)
        self.__base_index = KmerSetTypeMap[k](str(path))
        self.__k = k

    @property
    def k(self):
        return self.__k

    def __contains__(self, kmer: KmerType | Kmer):
        if isinstance(kmer, KmerType):
            return kmer in self.__base_index
        return kmer.base_type in self.__base_index

    def __len__(self):
        return len(self.__base_index)

    def __iter__(self):
        yield from self.__base_index

    @classmethod
    def build(
        cls,
        iterator: Iterator[Kmer | KmerType],
        index_path: Path,
        k: int,
        buffer_size=10**7,
    ) -> Self:
        BaseIndexType = KmerSetTypeMap[k]
        if index_path.exists():
            raise IOError("path already exists")
        iterator = map(
            lambda e: getattr(e, "base_type", e),
            iterator,
        )
        breakpoint()
        BaseIndexType.build(iterator, str(index_path), buffer_size=buffer_size)
        return cls(index_path, k)

    @classmethod
    def build_dna(
        cls,
        iterator: Iterator[DNA | rust_DNA],
        index_path: Path,
        k: int,
        index: int,
        modulo: int,
        buffer_size=10**7,
    ) -> Self:
        BaseIndexType = KmerSetTypeMap[k]
        if index_path.exists():
            raise IOError("path already exists")
        iterator = map(
            lambda e: getattr(e, "data", e),
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
