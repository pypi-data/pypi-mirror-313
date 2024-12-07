use dyn_clone::DynClone;
use ndarray::NdFloat;

use crate::{
    boundary::AnyBoundary,
    model::any::{AnyExt, AnyModel},
    stepping::TimeStepping,
};

pub struct AnyTimeStepping<F: NdFloat> {
    stepping: Box<dyn 'static + ErasedTimeStepping<F> + Send + Sync>,
}

impl<F: NdFloat> AnyTimeStepping<F> {
    #[must_use]
    pub fn new<T: 'static + TimeStepping<AnyModel<F>, AnyBoundary<F>> + Clone + Send + Sync>(
        stepping: T,
    ) -> Self {
        Self {
            stepping: Box::new(stepping),
        }
    }
}

impl<F: NdFloat> TimeStepping<AnyModel<F>, AnyBoundary<F>> for AnyTimeStepping<F> {
    fn step(
        &mut self,
        model: &mut AnyModel<F>,
        ext: &mut AnyExt,
        boundary: &mut AnyBoundary<F>,
        dt: F,
    ) {
        self.stepping.step(model, ext, boundary, dt);
    }
}

impl<F: NdFloat> Clone for AnyTimeStepping<F> {
    fn clone(&self) -> Self {
        Self {
            stepping: dyn_clone::clone_box(&*self.stepping),
        }
    }
}

trait ErasedTimeStepping<F: NdFloat>: TimeStepping<AnyModel<F>, AnyBoundary<F>> + DynClone {}

impl<F: NdFloat, T: TimeStepping<AnyModel<F>, AnyBoundary<F>> + DynClone> ErasedTimeStepping<F>
    for T
{
}
