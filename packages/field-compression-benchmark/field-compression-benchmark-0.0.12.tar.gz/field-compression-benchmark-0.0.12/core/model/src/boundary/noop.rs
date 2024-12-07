use crate::{boundary::BoundaryCondition, model::StateViewMut};

#[derive(Clone, Copy)]
pub struct NoopBoundary;

impl<S: ?Sized + StateViewMut> BoundaryCondition<S> for NoopBoundary {
    fn apply(&mut self, _state: &mut S) {
        // no-op
    }
}
