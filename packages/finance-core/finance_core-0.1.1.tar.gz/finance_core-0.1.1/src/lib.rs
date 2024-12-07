use pyo3::prelude::*;

mod sma;

use sma::TimeSeries;

/// Formats the sum of two numbers as string.
#[pyfunction]
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok((a + b).to_string())
}

/// A Python module implemented in Rust.
#[pymodule]
fn _finance_core(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<TimeSeries>()?;
    m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
    Ok(())
}
