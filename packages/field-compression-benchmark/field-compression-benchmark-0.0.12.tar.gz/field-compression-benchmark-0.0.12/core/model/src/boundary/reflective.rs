use ndarray::{SliceArg, SliceInfo, SliceInfoElem};

use crate::{boundary::BoundaryCondition, model::StateViewMut};

#[derive(Clone, Copy)]
pub struct ReflectiveBoundary<const N: usize>;

impl<S: ?Sized + StateViewMut, const N: usize> BoundaryCondition<S> for ReflectiveBoundary<N>
where
    for<'a> SliceInfo<&'a [SliceInfoElem], S::Dimension, S::Dimension>: SliceArg<S::Dimension>,
{
    fn apply(&mut self, state: &mut S) {
        for mut state in state.iter_mut() {
            let shape = state.shape().to_vec();

            let mut halo_slice = shape
                .iter()
                .map(|_| SliceInfoElem::from(..))
                .collect::<Vec<_>>();
            let mut edge_slice = shape
                .iter()
                .map(|_| SliceInfoElem::from(..))
                .collect::<Vec<_>>();

            #[allow(clippy::indexing_slicing, clippy::unwrap_used)] // FIXME
            for (i, len) in shape.into_iter().enumerate() {
                halo_slice[i] = SliceInfoElem::from(0..N);
                edge_slice[i] = SliceInfoElem::from(N..=N);

                let halo = SliceInfo::try_from(&halo_slice[..]).unwrap();
                let edge = SliceInfo::try_from(&edge_slice[..]).unwrap();

                let (mut halo_to, edge_from) = state.multi_slice_mut((halo, edge));
                halo_to.assign(&edge_from);
                std::mem::drop((halo_to, edge_from));

                edge_slice[i] = SliceInfoElem::from((len - N - 1)..(len - N));
                halo_slice[i] = SliceInfoElem::from((len - N)..);

                let edge = SliceInfo::try_from(&edge_slice[..]).unwrap();
                let halo = SliceInfo::try_from(&halo_slice[..]).unwrap();

                let (edge_from, mut halo_to) = state.multi_slice_mut((edge, halo));
                halo_to.assign(&edge_from);
                std::mem::drop((edge_from, halo_to));

                halo_slice[i] = SliceInfoElem::from(..);
                edge_slice[i] = SliceInfoElem::from(..);
            }
        }
    }
}

#[cfg(test)]
mod tests {
    use ndarray::ArrayViewMut;

    use crate::boundary::BoundaryCondition;

    use super::ReflectiveBoundary;

    #[test]
    #[allow(clippy::float_cmp)]
    fn reflective_1d() {
        let data = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0];

        let mut state = data;
        ReflectiveBoundary::<0>.apply(&mut ArrayViewMut::from(&mut state));
        assert_eq!(state, data);

        let mut state = data;
        ReflectiveBoundary::<1>.apply(&mut ArrayViewMut::from(&mut state));
        assert_eq!(state, [2.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 8.0]);

        let mut state = data;
        ReflectiveBoundary::<2>.apply(&mut ArrayViewMut::from(&mut state));
        assert_eq!(state, [3.0, 3.0, 3.0, 4.0, 5.0, 6.0, 7.0, 7.0, 7.0]);
    }
}
