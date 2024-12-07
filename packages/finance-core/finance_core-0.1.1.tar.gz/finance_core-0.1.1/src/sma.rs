use pyo3::prelude::*;

#[pyclass]
pub struct TimeSeries {
    pub index: Vec<i64>,
    pub values: Vec<f64>,
}

#[pymethods]
impl TimeSeries {
    #[new]
    pub fn new(index: Vec<i64>, values: Vec<f64>) -> Self {
        let mut index_size = 1;
        for i in 1..index.len() {
            if index[i] <= index[i - 1] {
                break;
            }
            index_size = i + 1;
        }
        if index_size != index.len() || index_size != values.len() {
            let size = std::cmp::min(index_size, values.len());
            TimeSeries {
                index: (&index[0..size]).to_vec(),
                values: (&values[0..size]).to_vec(),
            }
        } else {
            TimeSeries {
                index,
                values: (&values).to_vec(),
            }
        }
    }

    pub fn len(&self) -> usize {
        self.index.len()
    }

    pub fn sma(&self, window_size: usize) -> Vec<Option<f64>> {
        if window_size == 0 || self.values.is_empty() {
            return vec![];
        }

        let mut sma_values = Vec::with_capacity(self.values.len());
        let mut sum = 0.0;

        for i in 0..self.values.len() {
            sum += self.values[i];
            if i >= window_size {
                sum -= self.values[i - window_size];
            }

            if i >= window_size - 1 {
                sma_values.push(Some(sum / window_size as f64));
            } else {
                sma_values.push(None)
            }
        }

        sma_values
    }
}
