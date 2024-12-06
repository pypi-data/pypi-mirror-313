use pyo3::prelude::*;

#[pyfunction]
pub fn calculate_return(initial_investment: f64, final_value: f64) -> PyResult<f64> {
    let percentage_return = (final_value - initial_investment) / initial_investment;

    Ok(percentage_return)
}
