pub trait Reset {
    fn reset(&mut self);
}

pub trait Period {
    fn period(&self) -> usize;
}

pub trait Next<T> {
    type Output;
    fn next(&mut self, input: T) -> Self::Output;
}
