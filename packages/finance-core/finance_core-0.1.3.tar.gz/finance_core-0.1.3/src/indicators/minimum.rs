use pyo3::prelude::*;

use crate::traits::{Next, Period, Reset};

#[pyclass]
pub struct Minimum {
    period: usize,
    min_index: usize,
    cur_index: usize,
    deque: Vec<f64>,
}

#[pymethods]
impl Minimum {
    #[new]
    pub fn new(period: usize) -> Self {
        Self {
            period,
            min_index: 0,
            cur_index: 0,
            deque: vec![f64::INFINITY; period],
        }
    }

    pub fn period(&mut self) -> usize {
        Period::period(self)
    }

    pub fn next(&mut self, input: f64) -> f64 {
        Next::next(self, input)
    }

    pub fn reset(&mut self) {
        Reset::reset(self)
    }

    pub fn find_min_index(&self) -> usize {
        let mut min = f64::INFINITY;
        let mut index: usize = 0;

        for (i, &val) in self.deque.iter().enumerate() {
            if val < min {
                min = val;
                index = i;
            }
        }

        index
    }
}

impl Period for Minimum {
    fn period(&self) -> usize {
        self.period
    }
}

impl Next<f64> for Minimum {
    type Output = f64;

    fn next(&mut self, input: f64) -> Self::Output {
        self.deque[self.cur_index] = input;

        if input < self.deque[self.min_index] {
            self.min_index = self.cur_index;
        } else if self.min_index == self.cur_index {
            self.min_index = self.find_min_index();
        }

        self.cur_index = if self.cur_index + 1 < self.period {
            self.cur_index + 1
        } else {
            0
        };

        self.deque[self.min_index]
    }
}

impl Reset for Minimum {
    fn reset(&mut self) {
        for i in 0..self.period {
            self.deque[i] = f64::NEG_INFINITY;
        }
    }
}
