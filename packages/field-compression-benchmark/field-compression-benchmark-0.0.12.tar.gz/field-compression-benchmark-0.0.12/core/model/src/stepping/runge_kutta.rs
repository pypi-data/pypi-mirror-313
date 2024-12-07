use crate::{
    boundary::BoundaryCondition,
    model::{Model, State, StateView, StateViewMut},
    num::{half, two},
    stepping::TimeStepping,
};

pub struct RungeKutta4<L: ?Sized + Model> {
    scratch1: L::State,
    scratch2: L::State,
    scratch3: L::State,
}

impl<L: ?Sized + Model> RungeKutta4<L> {
    #[must_use]
    pub fn new(model: &L) -> Self {
        Self {
            scratch1: model.state().to_owned(),
            scratch2: model.state().to_owned(),
            scratch3: model.state().to_owned(),
        }
    }
}

impl<L: ?Sized + Model> Clone for RungeKutta4<L> {
    fn clone(&self) -> Self {
        Self {
            scratch1: self.scratch1.clone(),
            scratch2: self.scratch2.clone(),
            scratch3: self.scratch3.clone(),
        }
    }
}

impl<
        L: ?Sized + Model,
        B: ?Sized + for<'a> BoundaryCondition<<L::State as State>::ViewMut<'a>>,
    > TimeStepping<L, B> for RungeKutta4<L>
{
    fn step(&mut self, model: &mut L, ext: &mut L::Ext, boundary: &mut B, dt: L::Dtype) {
        // model.state = X_n

        let ext_backup = L::Ext::clone(ext);

        // k1 = X'(X_n)
        let k1 = &mut self.scratch1;
        model.tendencies(k1.view_mut(), ext);
        *ext = ext_backup.clone();

        // k_sum = k1
        let k_sum = &mut self.scratch3;
        k_sum.assign(k1.view());

        // k2 = X'(X_n + k1 * dt/2)
        let k1_dt = k1;
        k1_dt.mul_assign(dt * half::<L::Dtype>());
        k1_dt.add_assign(model.state());
        boundary.apply(&mut k1_dt.view_mut());
        let k2 = &mut self.scratch2;
        model.tendencies_for_state(k1_dt.view(), k2.view_mut(), ext);
        *ext = ext_backup.clone();

        // k_sum = k1 + 2*k2
        k_sum.add_assign(k2.view());
        k_sum.add_assign(k2.view());

        // k3 = X'(X_n + k2 * dt/2)
        let k2_dt = k2;
        k2_dt.mul_assign(dt * half::<L::Dtype>());
        k2_dt.add_assign(model.state());
        boundary.apply(&mut k2_dt.view_mut());
        let k3 = &mut self.scratch1;
        model.tendencies_for_state(k2_dt.view(), k3.view_mut(), ext);
        *ext = ext_backup;

        // k_sum = k1 + 2*k2 + 2*k3
        k_sum.add_assign(k3.view());
        k_sum.add_assign(k3.view());

        // k4 = X'(X_n + k3 * dt)
        let k3_dt = k3;
        k3_dt.mul_assign(dt);
        k3_dt.add_assign(model.state());
        boundary.apply(&mut k3_dt.view_mut());
        let k4 = &mut self.scratch2;
        model.tendencies_for_state(k3_dt.view(), k4.view_mut(), ext);

        // k_sum = k1 + 2*k2 + 2*k3 + k4
        k_sum.add_assign(k4.view());

        // k_sum = (k1 + 2*k2 + 2*k3 + k4) * dt/6
        let six = two::<L::Dtype>() + two::<L::Dtype>() + two::<L::Dtype>();
        k_sum.mul_assign(dt / six);

        // X_(n+1) = X_n + (k1 + 2*k2 + 2*k3 + k4) * dt/6
        boundary.apply(model.state_mut().add_assign(k_sum.view()));
    }
}
