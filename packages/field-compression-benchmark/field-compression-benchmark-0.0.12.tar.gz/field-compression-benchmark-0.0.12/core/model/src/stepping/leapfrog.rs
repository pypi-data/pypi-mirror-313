use crate::{
    boundary::BoundaryCondition,
    model::{Model, State, StateView, StateViewMut},
    num::two,
    stepping::TimeStepping,
};

pub struct LeapFrog<L: ?Sized + Model> {
    state_prev: L::State,
    scratch: L::State,
}

impl<L: ?Sized + Model> LeapFrog<L> {
    #[must_use]
    pub fn new(model: &L, state_prev: L::State) -> Self {
        Self {
            state_prev,
            scratch: model.state().to_owned(),
        }
    }
}

impl<L: ?Sized + Model> Clone for LeapFrog<L> {
    fn clone(&self) -> Self {
        Self {
            state_prev: self.state_prev.clone(),
            scratch: self.scratch.clone(),
        }
    }
}

impl<
        L: ?Sized + Model,
        B: ?Sized + for<'a> BoundaryCondition<<L::State as State>::ViewMut<'a>>,
    > TimeStepping<L, B> for LeapFrog<L>
{
    fn step(&mut self, model: &mut L, ext: &mut L::Ext, boundary: &mut B, dt: L::Dtype) {
        // model.state = X_n
        // self.state_prev = X_(n-1)

        // X_(n+1) = X_(n-1) + 2 * X'_n * dt
        let x_np1 = &mut self.scratch;
        model.tendencies(x_np1.view_mut(), ext);
        x_np1.mul_assign(dt * two());
        x_np1.add_assign(self.state_prev.view());
        boundary.apply(&mut x_np1.view_mut());

        // self.state_prev = X_n
        self.state_prev.assign(model.state());

        // model.state = X_(n+1)
        model.state_mut().assign(x_np1.view());
    }
}
