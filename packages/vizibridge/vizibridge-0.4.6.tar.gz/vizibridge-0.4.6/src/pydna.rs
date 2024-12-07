use crate::pykmer::*;
use pyo3::prelude::*;
use pyo3::types::PyString;
use seq_macro::seq;
use vizitig_lib::dna::DNA;
use vizitig_lib::iterators::{CanonicalKmerIterator, KmerIterator};

/// A class wrapper around a DNA struct from vizicomp
#[pyclass(name = "DNA")]
#[derive(Clone)]
pub struct PyDNA {
    pub content: DNA,
}

seq!(N in 0..=31{

#[pymethods]
impl PyDNA {

    #[new]
    pub fn new(input_pystr: &Bound<'_,PyString>) -> PyResult<Self> {
        let input_str = input_pystr.to_str()?;
        let dna = input_str.as_bytes().try_into().unwrap();
        Ok(PyDNA {
            content: dna
        })
   }

    pub fn __repr__(&self) -> PyResult<String> {
        Ok(self.content.content.clone().into_iter().map(|u| char::from(u)).collect::<String>())
    }

    fn __len__(&self) -> PyResult<usize>{
        Ok(self.content.content.len())
    }

    /// get the Nucleotid as a char at a given index
    pub fn get_index(&self, index: usize) -> PyResult<char>{
        Ok(self.content.content[index].into())
    }

    /// get a slice of the DNA
    pub fn get_slice(&self, start: usize, stop: usize) -> PyResult<Self> {
        Ok(PyDNA {
            content: DNA {
                content: self.content.content.get(start..stop).unwrap().to_vec()
            }
        })
    }

    #(
    /// Enumerate canonical N-kmer
    fn enumerate_canonical_kmer~N(&self) -> PyResult<Vec<PyKmer~N>>{
        if self.content.content.len() < N {  // this trigger a warning for N=0 but hard to avoid with macro madness
            return Ok(vec![]);
        }
        let it : CanonicalKmerIterator<N, u64> = (&self.content).try_into().unwrap();
        Ok(it.map(|u| PyKmer~N{content: u }).collect())
    }
    /// Enumerate N-kmer
    fn enumerate_kmer~N(&self) -> PyResult<Vec<PyKmer~N>>{
        if self.content.content.len() < N { // this trigger a warning for N=0 but hard to avoid with macro madness
            return Ok(vec![]);
        }
        let it : KmerIterator<N, u64> = (&self.content).try_into().unwrap();
        Ok(it.map(|u| PyKmer~N{content: u }).collect())
    }

    /// Enumerate canonical N-kmer
    fn enumerate_canonical_long_kmer~N(&self) -> PyResult<Vec<PyLongKmer~N>>{
        if self.content.content.len() < 32 + N {
            return Ok(vec![]);
        }
        let it : CanonicalKmerIterator<{32 + N}, u128> = (&self.content).try_into().unwrap();
        Ok(it.map(|u| PyLongKmer~N{ content: u }).collect())
    }
    /// Enumerate N-kmer
    fn enumerate_long_kmer~N(&self) -> PyResult<Vec<PyLongKmer~N>>{
        if self.content.content.len() < 32 + N {
            return Ok(vec![]);
        }
        let it : KmerIterator<{32 + N}, u128> = (&self.content).try_into().unwrap();
        Ok(it.map(|u| PyLongKmer~N{content: u }).collect())
    }
    )*
}
});
