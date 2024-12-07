//! This is the main entry point of the lib
//! We materialized all types that could be usefull
//! As we have 64 of them (32 for u64 type and 32 for u128)
//! we use seq! macro to generate all that in a concise way.
//!
//! To expose novel code, add a new module and integrate it belows.

#![allow(non_local_definitions)]
use pyo3::prelude::*;
use seq_macro::seq;

pub mod pydna;
pub mod pyindex;
pub mod pykmer;
pub mod pykmer_index;

seq!(N in 0..=31{
#[pymodule]
fn _vizibridge(_py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
    #(
        m.add_class::<pykmer::PyKmer~N>()?;
        m.add_class::<pykmer::PyLongKmer~N>()?;
        m.add_class::<pykmer_index::KmerIndex~N>()?;
        m.add_class::<pykmer_index::LongKmerIndex~N>()?;
        m.add_class::<pykmer_index::KmerSet~N>()?;
        m.add_class::<pykmer_index::LongKmerSet~N>()?;
    )*
    m.add_class::<pydna::PyDNA>()?;
    m.add_class::<pyindex::IntSet>()?;
    m.add_class::<pyindex::IntIndex>()?;
    Ok(())
}});
