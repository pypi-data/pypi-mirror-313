use dyn_clone::DynClone;
use ndarray::NdFloat;

use crate::{boundary::BoundaryCondition, model::any::AnyStateViewMut};

pub struct AnyBoundary<F: NdFloat> {
    boundary: Box<dyn 'static + ErasedBoundaryCondition<F> + Send + Sync>,
}

impl<F: NdFloat> AnyBoundary<F> {
    #[must_use]
    pub fn new<
        B: 'static + for<'a> BoundaryCondition<AnyStateViewMut<'a, F>> + Clone + Send + Sync,
    >(
        boundary: B,
    ) -> Self {
        Self {
            boundary: Box::new(boundary),
        }
    }
}

impl<'a, F: NdFloat> BoundaryCondition<AnyStateViewMut<'a, F>> for AnyBoundary<F> {
    fn apply(&mut self, state: &mut AnyStateViewMut<'a, F>) {
        self.boundary.apply(state);
    }
}

impl<F: NdFloat> Clone for AnyBoundary<F> {
    fn clone(&self) -> Self {
        Self {
            boundary: dyn_clone::clone_box(&*self.boundary),
        }
    }
}

trait ErasedBoundaryCondition<F: NdFloat>:
    for<'a> BoundaryCondition<AnyStateViewMut<'a, F>> + DynClone
{
}

impl<F: NdFloat, B: for<'a> BoundaryCondition<AnyStateViewMut<'a, F>> + DynClone>
    ErasedBoundaryCondition<F> for B
{
}
