use crate::pydna::PyDNA;
use pyo3::prelude::*;
use pyo3::types::PyType;
use seq_macro::seq;
use vizitig_lib::dna::Nucleotid;
use vizitig_lib::kmer::{LongKmer, ShortKmer};

seq!(N in 0..=31{

/// A Wrapper around an efficient representation of a N-kmer
#[pyclass]
#[derive(Clone)]
pub struct PyKmer~N{
    pub content: ShortKmer<N>,
}

#[pymethods]
impl PyKmer~N{

    #[new]
    pub fn new(data: u64) -> PyResult<Self> {
        Ok( Self{
            content: data.into()
        })
   }

    #[staticmethod]
    fn size() -> PyResult<usize> {
        Ok(N)
    }

    #[classmethod]
    fn from_dna(_: &Bound<'_, PyType>, dna: &PyDNA) -> PyResult<Self>{
        let nucleotids : &[Nucleotid; N] = dna.content.content.first_chunk::<N>().unwrap();
        let kmer : ShortKmer<N> = nucleotids.try_into().unwrap();
        Ok(Self { content: kmer })
    }

    fn add_left_nucleotid(&self, n: char) -> PyResult<Self>{
        Ok(Self { content: self.content.append_left(n.try_into().unwrap()) })
    }

    fn add_right_nucleotid(&self, n: char) -> PyResult<Self>{
        Ok(Self { content: self.content.append(n.try_into().unwrap()) })
    }

    fn reverse_complement(&self) -> PyResult<Self>{
        Ok(Self { content: self.content.rc() })
    }

    fn canonical(&self) -> PyResult<Self>{
        Ok(Self { content: self.content.normalize() })
    }

    fn is_canonical(&self) -> PyResult<bool>{
        Ok(self.content == self.content.normalize())
    }

    #[getter]
    fn data(&self) -> PyResult<u64>{
        Ok(self.content.get_data())
    }

    fn __hash__(&self) -> PyResult<u64>{
        Ok(self.content.get_data())
    }

    fn __repr__(&self) -> PyResult<String>{
        Ok(format!("{}", &self.content))
    }

    fn __str__(&self) -> PyResult<String>{
        Ok((&self.content).into())
    }

    fn __lt__(&self, other: Self) -> PyResult<bool> {
        Ok(self.content <= other.content)
    }

    fn __gt__(&self, other: Self) -> PyResult<bool> {
        Ok(self.content >= other.content)
    }

    fn __eq__(&self, other: Self) -> PyResult<bool> {
        Ok(self.content == other.content)
    }
}
});

seq!(N in 0..=31{
#[pyclass]
#[derive(Clone)]
pub struct PyLongKmer~N{
    pub content: LongKmer<{32 + N}>,
}

#[pymethods]
impl PyLongKmer~N{
    #[new]
    pub fn new(data: u128) -> PyResult<Self> {
        Ok( Self{
            content: data.into()
        })
   }

    #[staticmethod]
    fn size() -> PyResult<usize> {
        Ok(32 + N)
    }

    #[classmethod]
    fn from_dna(_: &Bound<'_, PyType>, dna: &PyDNA) -> PyResult<Self>{
        let nucleotids : &[Nucleotid; 32 + N] = dna.content.content.first_chunk::<{32 + N}>().unwrap();
        let kmer : LongKmer<{ 32 + N }> = nucleotids.try_into().unwrap();
        Ok(Self { content: kmer })
    }

    fn add_left_nucleotid(&self, n: char) -> PyResult<Self>{
        Ok(Self { content: self.content.append_left(n.try_into().unwrap()) })
    }

    fn add_right_nucleotid(&self, n: char) -> PyResult<Self>{
        Ok(Self { content: self.content.append(n.try_into().unwrap()) })
    }

    fn reverse_complement(&self) -> PyResult<Self>{
        Ok(Self { content: self.content.rc() })
    }

    fn canonical(&self) -> PyResult<Self>{
        Ok(Self { content: self.content.normalize() })
    }

    fn is_canonical(&self) -> PyResult<bool>{
        Ok(self.content == self.content.normalize())
    }

    #[getter]
    fn data(&self) -> PyResult<u128>{
        Ok(self.content.get_data())
    }

    fn __hash__(&self) -> PyResult<u64>{
        Ok((self.content.get_data() % 2u128.pow(64)) as u64)
    }

    fn __repr__(&self) -> PyResult<String>{
        Ok(format!("{}", &self.content))
    }

    fn __str__(&self) -> PyResult<String>{
        Ok((&self.content).into())
    }

    fn __lt__(&self, other: Self) -> PyResult<bool> {
        Ok(self.content <= other.content)
    }

    fn __gt__(&self, other: Self) -> PyResult<bool> {
        Ok(self.content >= other.content)
    }
}
});
