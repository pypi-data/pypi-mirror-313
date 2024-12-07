use ndarray::{SliceArg, SliceInfo, SliceInfoElem};

use crate::{boundary::BoundaryCondition, model::StateViewMut};

#[derive(Clone, Copy)]
pub struct PeriodicBoundary<const N: usize>;

impl<S: ?Sized + StateViewMut, const N: usize> BoundaryCondition<S> for PeriodicBoundary<N>
where
    for<'a> SliceInfo<&'a [SliceInfoElem], S::Dimension, S::Dimension>: SliceArg<S::Dimension>,
{
    fn apply(&mut self, state: &mut S) {
        for mut state in state.iter_mut() {
            let shape = state.shape().to_vec();

            let mut left_slice = shape
                .iter()
                .map(|_| SliceInfoElem::from(..))
                .collect::<Vec<_>>();
            let mut right_slice = shape
                .iter()
                .map(|_| SliceInfoElem::from(..))
                .collect::<Vec<_>>();

            #[expect(clippy::indexing_slicing, clippy::unwrap_used)] // FIXME
            for (i, len) in shape.into_iter().enumerate() {
                left_slice[i] = SliceInfoElem::from(0..N);
                right_slice[i] = SliceInfoElem::from((len - 2 * N)..(len - N));

                let left = SliceInfo::try_from(&left_slice[..]).unwrap();
                let right = SliceInfo::try_from(&right_slice[..]).unwrap();

                let (mut left_to, right_from) = state.multi_slice_mut((left, right));
                left_to.assign(&right_from);
                std::mem::drop((left_to, right_from));

                left_slice[i] = SliceInfoElem::from(N..(2 * N));
                right_slice[i] = SliceInfoElem::from((len - N)..);

                let left = SliceInfo::try_from(&left_slice[..]).unwrap();
                let right = SliceInfo::try_from(&right_slice[..]).unwrap();

                let (left_from, mut right_to) = state.multi_slice_mut((left, right));
                right_to.assign(&left_from);
                std::mem::drop((left_from, right_to));

                left_slice[i] = SliceInfoElem::from(..);
                right_slice[i] = SliceInfoElem::from(..);
            }
        }
    }
}

#[cfg(test)]
mod tests {
    use ndarray::ArrayViewMut;

    use crate::boundary::BoundaryCondition;

    use super::PeriodicBoundary;

    #[test]
    #[expect(clippy::float_cmp)]
    fn periodic_1d() {
        let data = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0];

        let mut state = data;
        PeriodicBoundary::<0>.apply(&mut ArrayViewMut::from(&mut state));
        assert_eq!(state, data);

        let mut state = data;
        PeriodicBoundary::<1>.apply(&mut ArrayViewMut::from(&mut state));
        assert_eq!(state, [8.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 2.0]);

        let mut state = data;
        PeriodicBoundary::<2>.apply(&mut ArrayViewMut::from(&mut state));
        assert_eq!(state, [6.0, 7.0, 3.0, 4.0, 5.0, 6.0, 7.0, 3.0, 4.0]);
    }
}
