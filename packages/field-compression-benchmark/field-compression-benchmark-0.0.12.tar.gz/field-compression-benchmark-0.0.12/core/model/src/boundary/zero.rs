use ndarray::{Axis, RemoveAxis};
use num_traits::Zero;

use crate::{boundary::BoundaryCondition, model::StateViewMut};

#[derive(Clone, Copy)]
pub struct ZeroBoundary<const N: usize>;

impl<S: ?Sized + StateViewMut<Dimension: RemoveAxis>, const N: usize> BoundaryCondition<S>
    for ZeroBoundary<N>
{
    fn apply(&mut self, state: &mut S) {
        for mut state in state.iter_mut() {
            let shape = state.shape().to_vec();

            for (i, len) in shape.into_iter().enumerate() {
                for j in 0..N.min(len) {
                    for x in &mut state.index_axis_mut(Axis(i), j) {
                        *x = S::Dtype::zero();
                    }
                }

                for j in len.saturating_sub(N)..len {
                    for x in &mut state.index_axis_mut(Axis(i), j) {
                        *x = S::Dtype::zero();
                    }
                }
            }
        }
    }
}
