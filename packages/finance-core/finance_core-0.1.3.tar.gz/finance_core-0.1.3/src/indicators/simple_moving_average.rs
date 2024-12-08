use pyo3::prelude::*;

use crate::traits::{Next, Period, Reset};

#[pyclass]
pub struct SimpleMovingAverage {
    period: usize,
    index: usize,
    count: usize,
    sum: f64,
    deque: Vec<f64>,
}

#[pymethods]
impl SimpleMovingAverage {
    #[new]
    pub fn new(period: usize) -> Self {
        Self {
            period,
            index: 0,
            count: 0,
            sum: 0.0,
            deque: vec![0.0; period],
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
}

impl Period for SimpleMovingAverage {
    fn period(&self) -> usize {
        self.period
    }
}

impl Next<f64> for SimpleMovingAverage {
    type Output = f64;

    fn next(&mut self, input: f64) -> Self::Output {
        let old_value = self.deque[self.index];
        self.deque[self.index] = input;

        self.index = if self.index + 1 < self.period {
            self.index + 1
        } else {
            0
        };

        if self.count < self.period {
            self.count += 1
        };

        self.sum = self.sum - old_value + input;
        self.sum / (self.count as f64)
    }
}

impl Reset for SimpleMovingAverage {
    fn reset(&mut self) {
        self.index = 0;
        self.count = 0;
        self.sum = 0.0;
        for i in 0..self.period {
            self.deque[i] = 0.0;
        }
    }
}
