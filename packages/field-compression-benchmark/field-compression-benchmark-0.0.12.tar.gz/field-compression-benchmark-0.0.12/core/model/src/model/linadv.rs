use ndarray::{s, Array, Array1, ArrayView, ArrayViewMut, Ix1, NdFloat};

use crate::{
    boundary::{BoundaryCondition, ZeroBoundary},
    for_each,
    model::Model,
    num::two,
};

pub struct Linadv<F: NdFloat> {
    parameters: LinadvParameters<F>,
    h_m: Array1<F>,
}

impl<F: NdFloat> Linadv<F> {
    #[must_use]
    pub fn new(parameters: LinadvParameters<F>) -> Self {
        Self {
            parameters,
            h_m: Array1::zeros((parameters.x_dim,)),
        }
    }

    #[must_use]
    pub const fn parameters(&self) -> &LinadvParameters<F> {
        &self.parameters
    }
}

impl<F: NdFloat> Model for Linadv<F> {
    type Dimension = Ix1;
    type Dtype = F;
    type Ext = ();
    type State = Array<F, Ix1>;

    fn variables(&self) -> impl Iterator<Item = &'static str> {
        ["h_m"].into_iter()
    }

    fn state(&self) -> ArrayView<Self::Dtype, Self::Dimension> {
        self.h_m.view()
    }

    fn state_mut(&mut self) -> ArrayViewMut<Self::Dtype, Self::Dimension> {
        self.h_m.view_mut()
    }

    fn tendencies_for_state(
        &self,
        state: ArrayView<Self::Dtype, Self::Dimension>,
        tendencies: ArrayViewMut<Self::Dtype, Self::Dimension>,
        _ext: &mut Self::Ext,
    ) {
        let LinadvParameters {
            x_dim: _,
            dx_m,
            U_const_m_s,
        } = self.parameters;

        let h_m = state;
        let mut h_tend_m_s = tendencies;

        // set the tendency boundary values to zero
        ZeroBoundary::<1>.apply(&mut h_tend_m_s);

        for_each!((
            dhdt in h_tend_m_s.slice_mut(s![1..-1]),

            &h_m1 in h_m.slice(s![..-2]),
            &h_p1 in h_m.slice(s![2..]),
        ) {
            *dhdt = -(U_const_m_s * (h_p1 - h_m1) / (dx_m * two()));
        });
    }

    fn with_state(&self, h_m: Array<Self::Dtype, Self::Dimension>) -> Self {
        let mut model = Self::new(self.parameters);
        model.h_m.view_mut().assign(&h_m);
        model
    }
}

#[derive(Clone, Copy, serde::Serialize, serde::Deserialize)]
#[expect(non_snake_case)]
pub struct LinadvParameters<F: NdFloat> {
    pub x_dim: usize,
    pub dx_m: F,
    pub U_const_m_s: F,
}
