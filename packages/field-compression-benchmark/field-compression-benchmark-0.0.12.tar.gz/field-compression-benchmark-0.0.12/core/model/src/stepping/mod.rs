use crate::{
    boundary::BoundaryCondition,
    model::{Model, State},
};

mod any;
mod forward_euler;
mod heun;
mod leapfrog;
mod runge_kutta;

pub use any::AnyTimeStepping;
pub use forward_euler::ForwardEuler;
pub use heun::Heun;
pub use leapfrog::LeapFrog;
pub use runge_kutta::RungeKutta4;

pub trait TimeStepping<
    L: ?Sized + Model,
    B: ?Sized + for<'a> BoundaryCondition<<L::State as State>::ViewMut<'a>>,
>
{
    fn step(&mut self, model: &mut L, ext: &mut L::Ext, boundary: &mut B, dt: L::Dtype);
}
