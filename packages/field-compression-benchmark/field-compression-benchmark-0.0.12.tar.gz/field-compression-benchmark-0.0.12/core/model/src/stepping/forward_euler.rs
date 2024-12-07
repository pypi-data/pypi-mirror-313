use crate::{
    boundary::BoundaryCondition,
    model::{Model, State, StateView, StateViewMut},
    stepping::TimeStepping,
};

pub struct ForwardEuler<L: ?Sized + Model> {
    scratch: L::State,
}

impl<L: ?Sized + Model> ForwardEuler<L> {
    #[must_use]
    pub fn new(model: &L) -> Self {
        Self {
            scratch: model.state().to_owned(),
        }
    }
}

impl<L: ?Sized + Model> Clone for ForwardEuler<L> {
    fn clone(&self) -> Self {
        Self {
            scratch: self.scratch.clone(),
        }
    }
}

impl<
        L: ?Sized + Model,
        B: ?Sized + for<'a> BoundaryCondition<<L::State as State>::ViewMut<'a>>,
    > TimeStepping<L, B> for ForwardEuler<L>
{
    fn step(&mut self, model: &mut L, ext: &mut L::Ext, boundary: &mut B, dt: L::Dtype) {
        // model.state = X_n

        // X_(n+1) = X_n + X'_n * dt
        let x_np1 = &mut self.scratch;
        model.tendencies(x_np1.view_mut(), ext);
        x_np1.mul_assign(dt);
        boundary.apply(model.state_mut().add_assign(x_np1.view()));
    }
}
