use crate::{
    boundary::BoundaryCondition,
    model::{Model, State, StateView, StateViewMut},
    num::half,
    stepping::TimeStepping,
};

pub struct Heun<L: ?Sized + Model> {
    scratch1: L::State,
    scratch2: L::State,
}

impl<L: ?Sized + Model> Heun<L> {
    #[must_use]
    pub fn new(model: &L) -> Self {
        Self {
            scratch1: model.state().to_owned(),
            scratch2: model.state().to_owned(),
        }
    }
}

impl<L: ?Sized + Model> Clone for Heun<L> {
    fn clone(&self) -> Self {
        Self {
            scratch1: self.scratch1.clone(),
            scratch2: self.scratch2.clone(),
        }
    }
}

impl<
        L: ?Sized + Model,
        B: ?Sized + for<'a> BoundaryCondition<<L::State as State>::ViewMut<'a>>,
    > TimeStepping<L, B> for Heun<L>
{
    fn step(&mut self, model: &mut L, ext: &mut L::Ext, boundary: &mut B, dt: L::Dtype) {
        // X_n
        let x_n = &mut self.scratch1;
        x_n.assign(model.state());
        // model.state = X_n

        // X_(n+1) = X_n + X'_n * dt
        let x_np1 = &mut self.scratch2;
        model.tendencies(x_np1.view_mut(), ext);
        x_np1.mul_assign(dt);
        boundary.apply(model.state_mut().add_assign(x_np1.view()));
        // model.state = X_(n+1)

        // X_(n+2) = X_(n+1) + X'(n+1) * dt
        let x_np2 = &mut self.scratch2;
        model.tendencies(x_np2.view_mut(), ext);
        x_np2.mul_assign(dt);
        boundary.apply(model.state_mut().add_assign(x_np2.view()));
        // model.state = X_(n+2)

        // X_(n+1) = (X_n + X_(n+2)) * 0.5
        boundary.apply(
            model
                .state_mut()
                .add_assign(x_n.view())
                .mul_assign(half::<L::Dtype>()),
        );
    }
}
