use crate::pydna::PyDNA;
use crate::pyindex::{IntIndex, IntSet};
use crate::pykmer::*;
use pyo3::exceptions::PyKeyError;
use pyo3::prelude::*;
use pyo3::types::{PyIterator, PyString, PyType};
use seq_macro::seq;
use std::path::Path;
use vizitig_lib::iterators::CanonicalKmerIterator;
use vizitig_lib::kmer::Kmer;
use vizitig_lib::dna::DNA;
use vizitig_lib::kmer_index::{IndexIterator, KmerIndex, KmerIndexEntry};

seq!(N in 0..=31{

#[pyclass]
#[derive(Clone)]
pub struct KmerIndexEntry~N{
    pub inner: KmerIndexEntry::<N, u64, u32>,
}

#[pymethods]
impl KmerIndexEntry~N{
    #[new]
    fn new(kmer: PyKmer~N, val: u32) -> Self{
        Self {
            inner: KmerIndexEntry::<N, u64, u32>{
                key: kmer.content,
                val: val
            }
        }
    }

    #[staticmethod]
    fn size() -> PyResult<usize> {
        Ok(N)
    }

    #[getter]
    fn kmer(&self) -> PyResult<PyKmer~N>{
        Ok(PyKmer~N{
            content: self.inner.key
        })
    }

    #[getter]
    fn val(&self) -> PyResult<u32>{
        Ok(self.inner.val)
    }
}


#[pyclass]
#[derive(Clone)]
pub struct KmerIndex~N{
    pub index: KmerIndex<N, u64, u32>,
}

#[pymethods]
impl KmerIndex~N{
    #[classmethod]
    pub fn build(_: &Bound<'_, PyType>, iterator: &Bound<'_, PyIterator>, index_path: &Bound<'_, PyString>, buffer_size: usize) -> PyResult<Self> {
        let path : &Path = Path::new(index_path.to_str()?);
        let kmer_entry_iter = iterator.try_iter()?.map(|i| i.and_then(|i|{
            let kmer = i.getattr("kmer")?.extract::<PyKmer~N>().unwrap().content;
            Ok(KmerIndexEntry::<N, u64, u32>{
                key: kmer,
                val: i.getattr("val")?.extract::<u32>().unwrap()
            })
            }));

        Ok(Self{
            index: KmerIndex::<N, u64, u32>::build_index(kmer_entry_iter.map(|e| e.unwrap()), path, buffer_size).unwrap(),
        })
    }

    #[classmethod]
    pub fn build_dna(_: &Bound<'_, PyType>, iterator: &Bound<'_, PyIterator>, index_path: &Bound<'_, PyString>, buffer_size: usize, index: u64, modulo: u64) -> PyResult<Self> {
        let path : &Path = Path::new(index_path.to_str()?);
        let dna_entry_iter = iterator.try_iter()?.map(|i| i.and_then(|i|{
            let dna = i.getattr("DNA")?.extract::<PyDNA>().unwrap().content;
            let val = i.getattr("val")?.extract::<u32>().unwrap();
            Ok((dna, val))
        }));
        let kmer_iter = dna_entry_iter.map(|e| e.unwrap()).map(|(dna, val)|{
            match <&DNA as TryInto<CanonicalKmerIterator<N, u64>>>::try_into(&dna){
                Ok(kmer_it)=> {
                    let kmer_vec: Vec<KmerIndexEntry::<N, u64, u32>> = kmer_it.filter(|kmer| kmer.get_data() % modulo == index).map(move |kmer| KmerIndexEntry::<N, u64, u32>{
                        key: kmer,
                        val: val
                    }).collect::<Vec<_>>();
                    kmer_vec.into_iter()
                },
                _ => {
                    vec![].into_iter()
                }
            }
        }).flatten();

        Ok(Self{
            index: KmerIndex::<N, u64, u32>::build_index(kmer_iter, path, buffer_size).unwrap(),
        })
    }

    pub fn join_iter32(&self,
            iterator: &Bound<'_, PyIterator>,
            out_path: &Bound<'_, PyString>,
            buffer_size: usize) -> PyResult<IntIndex>{
        let path: &Path = Path::new(out_path.to_str().unwrap());
        let parsed_iterator = iterator.try_iter()?.map(|i| i.and_then(|i|{
            Ok((i.getattr("kmer")?.extract::<PyKmer~N>().unwrap().content,
                i.getattr("val")?.extract::<u32>().unwrap())
           )
        })).map(|e| e.unwrap());
        Ok(
            IntIndex{
                index: self.index.join_iter(parsed_iterator, path, buffer_size)
            })
    }

    pub fn intersection_iter32(&self,
            iterator: &Bound<'_, PyIterator>,
            out_path: &Bound<'_, PyString>,
            buffer_size: usize) -> PyResult<IntSet>{
        let path: &Path = Path::new(out_path.to_str().unwrap());
        let parsed_iterator = iterator.try_iter()?.map(|i| i.and_then(|i|{
            Ok((
                i.extract::<PyKmer~N>().unwrap().content,
                ()
            ))
           })).map(|e| e.unwrap());
           Ok(
               IntSet{
                   index: self.index.join_iter(parsed_iterator, path, buffer_size)
              })
    }

    pub fn intersection_index(&self,
        other: &KmerSet~N,
        out_path: &Bound<'_, PyString>,
        buffer_size: usize) -> PyResult<IntSet>{

        let path: &Path = Path::new(out_path.to_str().unwrap());
        Ok(IntSet {
            index:
                self.index.join_index::<()>(other.index.clone(), path, buffer_size)
        })
    }

    pub fn join_index(&self,
        other: &KmerIndex~N,
        out_path: &Bound<'_, PyString>,
        buffer_size: usize) -> PyResult<IntIndex>{

        let path: &Path = Path::new(out_path.to_str().unwrap());
        Ok(IntIndex {
            index:
                self.index.join_index::<u32>(other.index.clone(), path, buffer_size)
        })
    }



    pub fn __len__(&self) -> PyResult<usize>{
        Ok(self.index.len())
    }

    pub fn __getitem__(&self, kmer: PyKmer~N) -> PyResult<u32>{
        match self.index.get(kmer.content) {
            Ok(val) => Ok(val),
            _ => Err(PyKeyError::new_err(kmer))
        }
    }

    #[new]
    fn new(index_path: &Bound<'_, PyString>) -> PyResult<Self>{
        let path : &Path = Path::new(index_path.to_str()?);
        Ok(Self{
            index: KmerIndex::<N, u64, u32>::load_index(path).unwrap()
        })
    }


    fn __iter__(slf: PyRef<Self>) -> PyResult<Py<IndexIterator~N>> {
        let iter = IndexIterator~N {
            inner: slf.index.clone().into_iter(),
        };
        Py::new(slf.py(), iter)
    }

    #[staticmethod]
    fn size() -> PyResult<usize> {
        Ok(N)
    }

}
#[pyclass]
pub struct IndexIterator~N{
    pub inner: IndexIterator<Kmer<N, u64>, u32>
}


#[pymethods]
impl IndexIterator~N {
    fn __iter__(slf: PyRef<Self>) -> PyRef<Self> {
        slf
    }

    fn __next__(mut slf: PyRefMut<Self>) -> Option<KmerIndexEntry~N> {
        match slf.inner.next(){
            Some(index_entry) => {
                Some(KmerIndexEntry~N {
                    inner: index_entry
                })
            },
            _ => None
        }
    }
}

#[pyclass]
#[derive(Clone)]
pub struct KmerSet~N{
    pub index: KmerIndex<N, u64, ()>,
}

#[pymethods]
impl KmerSet~N{
    #[classmethod]
    pub fn build(_: &Bound<'_, PyType>, iterator: &Bound<'_, PyIterator>, index_path: &Bound<'_, PyString>, buffer_size: usize) -> PyResult<Self> {
        let path : &Path = Path::new(index_path.to_str()?);
        let kmer_entry_iter = iterator.try_iter()?.map(|i| i.and_then(|i|{
            let kmer = i.extract::<PyKmer~N>().unwrap().content;
            Ok(KmerIndexEntry::<N, u64, ()>{
                key: kmer,
                val: ()
            })
            }));

        Ok(Self{
            index: KmerIndex::<N, u64, ()>::build_index(kmer_entry_iter.map(|e| e.unwrap()), path, buffer_size).unwrap(),
        })
    }

    #[classmethod]
    pub fn build_dna(_: &Bound<'_, PyType>, iterator: &Bound<'_, PyIterator>, index_path: &Bound<'_, PyString>, buffer_size: usize, index: u64, modulo: u64) -> PyResult<Self> {
        let path : &Path = Path::new(index_path.to_str()?);
        let dna_entry_iter = iterator.try_iter()?.map(|i| i.and_then(|i|{
            let dna = i.extract::<PyDNA>().unwrap().content;
            Ok(dna)
        }));
        let kmer_iter = dna_entry_iter.map(|e| e.unwrap()).map(|dna|{
            match <&DNA as TryInto<CanonicalKmerIterator<N, u64>>>::try_into(&dna){
                Ok(kmer_it)=> {
                    let kmer_vec: Vec<KmerIndexEntry::<N, u64, ()>> = kmer_it.filter(|kmer| kmer.get_data() % modulo == index)
                                    .map(move |kmer| KmerIndexEntry::<N, u64, ()>{
                        key: kmer,
                        val: ()
                    }).collect::<Vec<_>>();
                    kmer_vec.into_iter()
                },
                _ => {
                    vec![].into_iter()
                }
            }
        }).flatten();

        Ok(Self{
            index: KmerIndex::<N, u64, ()>::build_index(kmer_iter, path, buffer_size).unwrap(),
        })
    }
    pub fn __len__(&self) -> PyResult<usize>{
        Ok(self.index.len())
    }

    pub fn __contains__(&self, kmer: PyKmer~N) -> PyResult<bool>{
        match self.index.get(kmer.content){
            Ok(_) => Ok(true),
            _ => Ok(false)
        }
    }

    #[new]
    fn new(index_path: &Bound<'_, PyString>) -> PyResult<Self>{
        let path : &Path = Path::new(index_path.to_str()?);
        Ok(Self{
            index: KmerIndex::<N, u64, ()>::load_index(path).unwrap()
        })
    }


    fn __iter__(slf: PyRef<Self>) -> PyResult<Py<IndexSetIterator~N>> {
        let iter = IndexSetIterator~N {
            inner: slf.index.clone().into_iter(),
        };
        Py::new(slf.py(), iter)
    }

    #[staticmethod]
    fn size() -> PyResult<usize> {
        Ok(N)
    }

}




#[pyclass]
pub struct IndexSetIterator~N{
    pub inner: IndexIterator<Kmer<N, u64>, ()>
}


#[pymethods]
impl IndexSetIterator~N {
    fn __iter__(slf: PyRef<Self>) -> PyRef<Self> {
        slf
    }

    fn __next__(mut slf: PyRefMut<Self>) -> Option<PyKmer~N> {
        match slf.inner.next(){
            Some(index_entry) => {
                Some(PyKmer~N{
                    content: index_entry.key
                })
            },
            _ => None
        }
    }
}

});

// Long version

seq!(N in 0..=31{

#[pyclass]
#[derive(Clone)]
pub struct LongKmerIndexEntry~N{
    pub inner: KmerIndexEntry::<{ N+32 }, u128, u32>,
}

#[pymethods]
impl LongKmerIndexEntry~N{
    #[new]
    fn new(kmer: PyLongKmer~N, val: u32) -> Self{
        Self {
            inner: KmerIndexEntry::<{ N+32 }, u128, u32>{
                key: kmer.content,
                val: val
            }
        }
    }

    #[staticmethod]
    fn size() -> PyResult<usize> {
        Ok(N+32)
    }

    #[getter]
    fn kmer(&self) -> PyResult<PyLongKmer~N>{
        Ok(PyLongKmer~N{
            content: self.inner.key
        })
    }

    #[getter]
    fn val(&self) -> PyResult<u32>{
        Ok(self.inner.val)
    }
}


#[pyclass]
#[derive(Clone)]
pub struct LongKmerIndex~N{
    pub index: KmerIndex<{N + 32}, u128, u32>,
}

#[pymethods]
impl LongKmerIndex~N{
    #[classmethod]
    pub fn build(_: &Bound<'_, PyType>, iterator: &Bound<'_, PyIterator>, index_path: &Bound<'_, PyString>, buffer_size: usize) -> PyResult<Self> {
        let path : &Path = Path::new(index_path.to_str()?);
        let kmer_entry_iter = iterator.try_iter()?.map(|i| i.and_then(|i|
            Ok(KmerIndexEntry::<{N+32}, u128, u32>{
                key: i.getattr("kmer")?.extract::<PyLongKmer~N>().unwrap().content,
                val: i.getattr("val")?.extract::<u32>().unwrap()
            })));

        Ok(Self{
            index: KmerIndex::<{N +32}, u128, u32>::build_index(kmer_entry_iter.filter_map(|e| e.ok()), path, buffer_size).unwrap(),
        })
    }

    #[classmethod]
    pub fn build_dna(_: &Bound<'_, PyType>, iterator: &Bound<'_, PyIterator>, index_path: &Bound<'_, PyString>, buffer_size: usize, index: u64, modulo: u64) -> PyResult<Self> {
        let path : &Path = Path::new(index_path.to_str()?);
        let dna_entry_iter = iterator.try_iter()?.map(|i| i.and_then(|i|{
            let dna = i.getattr("DNA")?.extract::<PyDNA>().unwrap().content;
            let val = i.getattr("val")?.extract::<u32>().unwrap();
            Ok((dna, val))
        }));
        let kmer_iter = dna_entry_iter.map(|e| e.unwrap()).map(|(dna, val)|{
            match <&DNA as TryInto<CanonicalKmerIterator<{N+32}, u128>>>::try_into(&dna){
                Ok(kmer_it)=> {
                    let kmer_vec: Vec<KmerIndexEntry::<{N+32}, u128, u32>> = kmer_it.filter(|kmer| (kmer.get_data() % (modulo as u128)) as u64 == index)
                                    .map(move |kmer| KmerIndexEntry::<{N+32}, u128, u32>{
                        key: kmer,
                        val: val
                    }).collect::<Vec<_>>();
                    kmer_vec.into_iter()
                },
                _ => {
                    vec![].into_iter()
                }
            }
        }).flatten();

        Ok(Self{
            index: KmerIndex::<{N+32}, u128, u32>::build_index(kmer_iter, path, buffer_size).unwrap(),
        })
    }

    pub fn join_iter32(&self,
            iterator: &Bound<'_, PyIterator>,
            out_path: &Bound<'_, PyString>,
            buffer_size: usize) -> PyResult<IntIndex>{
        let path: &Path = Path::new(out_path.to_str().unwrap());
        let parsed_iterator = iterator.try_iter()?.map(|i| i.and_then(|i|{
            Ok((i.getattr("kmer")?.extract::<PyLongKmer~N>().unwrap().content,
                i.getattr("val")?.extract::<u32>().unwrap())
           )
        })).map(|e| e.unwrap());
        Ok(
            IntIndex{
                index: self.index.join_iter(parsed_iterator, path, buffer_size)
            })
    }

    pub fn intersection_iter32(&self,
            iterator: &Bound<'_, PyIterator>,
            out_path: &Bound<'_, PyString>,
            buffer_size: usize) -> PyResult<IntSet>{
        let path: &Path = Path::new(out_path.to_str().unwrap());
        let parsed_iterator = iterator.try_iter()?.map(|i| i.and_then(|i|{
            Ok((
                i.extract::<PyLongKmer~N>().unwrap().content,
                ()
            ))
           })).map(|e| e.unwrap());
           Ok(
               IntSet{
                   index: self.index.join_iter(parsed_iterator, path, buffer_size)
              })
    }

    pub fn intersection_index(&self,
        other: &LongKmerSet~N,
        out_path: &Bound<'_, PyString>,
        buffer_size: usize) -> PyResult<IntSet>{

        let path: &Path = Path::new(out_path.to_str().unwrap());
        Ok(IntSet {
            index:
                self.index.join_index::<()>(other.index.clone(), path, buffer_size)
        })
    }

    pub fn join_index(&self,
        other: &LongKmerIndex~N,
        out_path: &Bound<'_, PyString>,
        buffer_size: usize) -> PyResult<IntIndex>{

        let path: &Path = Path::new(out_path.to_str().unwrap());
        Ok(IntIndex {
            index:
                self.index.join_index::<u32>(other.index.clone(), path, buffer_size)
        })
    }


    fn __len__(&self) -> PyResult<usize>{
        Ok(self.index.len())
    }

    fn __getitem__(&self, kmer: PyLongKmer~N) -> PyResult<u32>{
        match self.index.get(kmer.content){
            Ok(val) => Ok(val),
            _ => Err(PyKeyError::new_err(kmer))
        }
    }

    #[staticmethod]
    fn size() -> PyResult<usize> {
        Ok(N+32)
    }
    #[new]
    fn new(index_path: &Bound<'_, PyString>) -> PyResult<Self>{
        let path : &Path = Path::new(index_path.to_str()?);
        Ok(Self{
            index: KmerIndex::<{N + 32}, u128, u32>::load_index(path).unwrap()
        })
    }


    fn __iter__(slf: PyRef<Self>) -> PyResult<Py<LongIndexIterator~N>> {
        let iter = LongIndexIterator~N {
            inner: slf.index.clone().into_iter(),
        };
        Py::new(slf.py(), iter)
    }

}


#[pyclass]
pub struct LongIndexIterator~N{
    pub inner: IndexIterator<Kmer<{N + 32}, u128>, u32>
}


#[pymethods]
impl LongIndexIterator~N {
    fn __iter__(slf: PyRef<Self>) -> PyRef<Self> {
        slf
    }

    fn __next__(mut slf: PyRefMut<Self>) -> Option<LongKmerIndexEntry~N> {
        match slf.inner.next(){
            Some(index_entry) => {
                Some(LongKmerIndexEntry~N {
                    inner: index_entry
                })
            },
            _ => None
        }
    }
}
#[pyclass]
#[derive(Clone)]
pub struct LongKmerSet~N{
    pub index: KmerIndex<{N + 32}, u128, ()>,
}

#[pymethods]
impl LongKmerSet~N{
    #[classmethod]
    pub fn build(_: &Bound<'_, PyType>, iterator: &Bound<'_, PyIterator>, index_path: &Bound<'_, PyString>, buffer_size: usize) -> PyResult<Self> {
        let path : &Path = Path::new(index_path.to_str()?);
        let kmer_entry_iter = iterator.try_iter()?.map(|i| i.and_then(|i|{
            let kmer = i.extract::<PyLongKmer~N>().unwrap().content;
            Ok(KmerIndexEntry::<{ N + 32}, u128, ()>{
                key: kmer,
                val: ()
            })
            }));

        Ok(Self{
            index: KmerIndex::<{ N + 32}, u128, ()>::build_index(kmer_entry_iter.map(|e| e.unwrap()), path, buffer_size).unwrap(),
        })
    }

    #[classmethod]
    pub fn build_dna(
        _: &Bound<'_, PyType>,
        iterator: &Bound<'_, PyIterator>,
        index_path: &Bound<'_, PyString>,
        buffer_size: usize,
        index: u64,
        modulo: u64
    ) -> PyResult<Self> {
        let path : &Path = Path::new(index_path.to_str()?);
        let dna_entry_iter = iterator.try_iter()?.map(|i| i.and_then(|i|{
            let dna = i.extract::<PyDNA>().unwrap().content;
            Ok(dna)
        }));
        let kmer_iter = dna_entry_iter.map(|e| e.unwrap()).map(|dna|{
            match <&DNA as TryInto<CanonicalKmerIterator<{N+32}, u128>>>::try_into(&dna){
                Ok(kmer_it)=> {
                    let kmer_vec: Vec<KmerIndexEntry::<{N+32}, u128, ()>> = kmer_it.filter(|kmer| (kmer.get_data() % (modulo as u128)) as u64 == index)
                                    .map(move |kmer| KmerIndexEntry::<{N+32}, u128, ()>{
                        key: kmer,
                        val: ()
                    }).collect::<Vec<_>>();
                    kmer_vec.into_iter()
                },
                _ => {
                    vec![].into_iter()
                }
            }
        }).flatten();

        Ok(Self{
            index: KmerIndex::<{ N + 32}, u128, ()>::build_index(kmer_iter, path, buffer_size).unwrap(),
        })
    }
    pub fn __len__(&self) -> PyResult<usize>{
        Ok(self.index.len())
    }

    pub fn __contains__(&self, kmer: PyLongKmer~N) -> PyResult<bool>{
        match self.index.get(kmer.content){
            Ok(_) => Ok(true),
            _ => Ok(false)
        }
    }

    #[new]
    fn new(index_path: &Bound<'_, PyString>) -> PyResult<Self>{
        let path : &Path = Path::new(index_path.to_str()?);
        Ok(Self{
            index: KmerIndex::<{N+32}, u128, ()>::load_index(path).unwrap()
        })
    }


    fn __iter__(slf: PyRef<Self>) -> PyResult<Py<IndexLongSetIterator~N>> {
        let iter = IndexLongSetIterator~N {
            inner: slf.index.clone().into_iter(),
        };
        Py::new(slf.py(), iter)
    }

    #[staticmethod]
    fn size() -> PyResult<usize> {
        Ok(N + 32)
    }

}




#[pyclass]
pub struct IndexLongSetIterator~N{
    pub inner: IndexIterator<Kmer<{N + 32}, u128>, ()>
}


#[pymethods]
impl IndexLongSetIterator~N {
    fn __iter__(slf: PyRef<Self>) -> PyRef<Self> {
        slf
    }

    fn __next__(mut slf: PyRefMut<Self>) -> Option<PyLongKmer~N> {
        match slf.inner.next(){
            Some(index_entry) => {
                Some(PyLongKmer~N{
                    content: index_entry.key
                })
            },
            _ => None
        }
    }
}

});
