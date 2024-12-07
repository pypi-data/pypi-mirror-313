use pyo3::exceptions::PyKeyError;
use pyo3::prelude::*;
use pyo3::types::{PyIterator, PyString, PyType};
use std::path::Path;
use vizitig_lib::kmer_index::{Index, IndexEntry, IndexIterator};

///! VERSION (u32, u32)

#[pyclass]
pub struct IndexIteratoru32u32 {
    pub inner: IndexIterator<u32, u32>,
}

#[pymethods]
impl IndexIteratoru32u32 {
    fn __iter__(slf: PyRef<Self>) -> PyRef<Self> {
        slf
    }

    fn __next__(mut slf: PyRefMut<Self>) -> Option<(u32, u32)> {
        match slf.inner.next() {
            Some(index_entry) => Some((index_entry.key, index_entry.val.try_into().unwrap())),
            _ => None,
        }
    }
}

#[pyclass]
#[derive(Clone)]
pub struct IntIndex {
    pub index: Index<u32, u32>,
}

#[pymethods]
impl IntIndex {
    #[classmethod]
    pub fn build(
        _: &Bound<'_, PyType>,
        iterator: &Bound<'_, PyIterator>,
        index_path: &Bound<'_, PyString>,
        buffer_size: usize,
    ) -> PyResult<Self> {
        let path: &Path = Path::new(index_path.to_str()?);
        let entry_iter = iterator.try_iter()?.map(|i| {
            i.and_then(|i| {
                Ok(IndexEntry::<u32, u32> {
                    key: i.getattr("key")?.extract::<u32>().unwrap(),
                    val: i.getattr("val")?.extract::<u32>().unwrap(),
                })
            })
        });

        Ok(Self {
            index: Index::<u32, u32>::build_index(
                entry_iter.map(|e| e.unwrap()),
                path,
                buffer_size,
            )
            .unwrap(),
        })
    }

    pub fn __len__(&self) -> PyResult<usize> {
        Ok(self.index.len())
    }

    pub fn __getitem__(&self, key: u32) -> PyResult<u32> {
        match self.index.get(key) {
            Ok(val) => Ok(val),
            _ => Err(PyKeyError::new_err(key)),
        }
    }

    #[new]
    fn new(index_path: &Bound<'_, PyString>) -> PyResult<Self> {
        let path: &Path = Path::new(index_path.to_str()?);
        Ok(Self {
            index: Index::<u32, u32>::load_index(path).unwrap(),
        })
    }

    fn __iter__(slf: PyRef<Self>) -> PyResult<Py<IndexIteratoru32u32>> {
        let iter = IndexIteratoru32u32 {
            inner: slf.index.clone().into_iter(),
        };
        Py::new(slf.py(), iter)
    }
}

///! VERSION (u32, ())

#[pyclass]
pub struct IndexIteratoru32 {
    pub inner: IndexIterator<u32, ()>,
}

#[pymethods]
impl IndexIteratoru32 {
    fn __iter__(slf: PyRef<Self>) -> PyRef<Self> {
        slf
    }

    fn __next__(mut slf: PyRefMut<Self>) -> Option<u32> {
        match slf.inner.next() {
            Some(index_entry) => Some(index_entry.key),
            _ => None,
        }
    }
}

#[pyclass]
#[derive(Clone)]
pub struct IntSet {
    pub index: Index<u32, ()>,
}

#[pymethods]
impl IntSet {
    #[classmethod]
    pub fn build(
        _: &Bound<'_, PyType>,
        iterator: &Bound<'_, PyIterator>,
        index_path: &Bound<'_, PyString>,
        buffer_size: usize,
    ) -> PyResult<Self> {
        let path: &Path = Path::new(index_path.to_str()?);
        let entry_iter = iterator.try_iter()?.map(|i| {
            i.and_then(|i| {
                Ok(IndexEntry::<u32, ()> {
                    key: i.getattr("key")?.extract::<u32>().unwrap(),
                    val: (),
                })
            })
        });

        Ok(Self {
            index: Index::<u32, ()>::build_index(entry_iter.map(|e| e.unwrap()), path, buffer_size)
                .unwrap(),
        })
    }

    pub fn __len__(&self) -> PyResult<usize> {
        Ok(self.index.len())
    }

    pub fn __getitem__(&self, key: u32) -> PyResult<()> {
        match self.index.get(key) {
            Ok(val) => Ok(val),
            _ => Err(PyKeyError::new_err(key)),
        }
    }

    pub fn __contains__(&self, key: u32) -> PyResult<bool> {
        match self.index.get(key) {
            Ok(_) => Ok(true),
            _ => Ok(false),
        }
    }

    #[new]
    fn new(index_path: &Bound<'_, PyString>) -> PyResult<Self> {
        let path: &Path = Path::new(index_path.to_str()?);
        Ok(Self {
            index: Index::<u32, ()>::load_index(path).unwrap(),
        })
    }

    fn __iter__(slf: PyRef<Self>) -> PyResult<Py<IndexIteratoru32>> {
        let iter = IndexIteratoru32 {
            inner: slf.index.clone().into_iter(),
        };
        Py::new(slf.py(), iter)
    }
}
