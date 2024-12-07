from vizibridge.DNA import DNA
from vizibridge.kmers import Kmer
from vizibridge.kmer_index import KmerIndex, KmerIndexEntry, DNAIndexEntry
from vizibridge.kmer_set import KmerSet

__all__ = ["DNA", "Kmer", "KmerIndex"]


def kmer_from_str(dna: str) -> Kmer:
    return Kmer.from_dna(next(DNA.from_str(dna)))
