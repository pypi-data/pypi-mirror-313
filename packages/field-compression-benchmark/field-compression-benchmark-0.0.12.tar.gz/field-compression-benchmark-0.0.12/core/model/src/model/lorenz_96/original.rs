use ndarray::{Array, Array1, ArrayView, ArrayViewMut, Ix1, NdFloat};

use crate::{
    for_each,
    model::{
        lorenz_96::{ForcingSampler, K},
        Model,
    },
};

pub struct Lorenz96<F: NdFloat, S: ForcingSampler<Dtype = F>> {
    parameters: Lorenz96Parameters<F, S>,
    state: Array1<F>,
}

impl<F: NdFloat, S: ForcingSampler<Dtype = F>> Lorenz96<F, S> {
    #[must_use]
    pub fn new(parameters: Lorenz96Parameters<F, S>) -> Self {
        let k = parameters.k;
        Self {
            parameters,
            state: Array1::zeros((k.get(),)),
        }
    }

    #[must_use]
    pub const fn parameters(&self) -> &Lorenz96Parameters<F, S> {
        &self.parameters
    }
}

impl<F: NdFloat, S: ForcingSampler<Dtype = F>> Model for Lorenz96<F, S> {
    type Dimension = Ix1;
    type Dtype = F;
    type Ext = S::Ext;
    type State = Array<F, Ix1>;

    fn variables(&self) -> impl Iterator<Item = &'static str> {
        ["X_k"].into_iter()
    }

    fn state(&self) -> ArrayView<Self::Dtype, Self::Dimension> {
        self.state.view()
    }

    fn state_mut(&mut self) -> ArrayViewMut<Self::Dtype, Self::Dimension> {
        self.state.view_mut()
    }

    fn tendencies_for_state(
        &self,
        state: ArrayView<Self::Dtype, Self::Dimension>,
        tendencies: ArrayViewMut<Self::Dtype, Self::Dimension>,
        ext: &mut Self::Ext,
    ) {
        let Lorenz96Parameters { k: _, forcing } = &self.parameters;

        for_each!((
            dxdt in tendencies,

            &x_m2 in state.iter().cycle().skip(state.len() - 2),
            &x_m1 in state.iter().cycle().skip(state.len() - 1),
            &x in state.iter(),
            &x_p1 in state.iter().cycle().skip(1),
        ) {
            *dxdt = -x_m2 * x_m1 + x_m1 * x_p1 - x + forcing.sample(ext);
        });
    }

    fn with_state(&self, state: Array<Self::Dtype, Self::Dimension>) -> Self {
        let mut model = Self::new(self.parameters.clone());
        model.state.view_mut().assign(&state);
        model
    }
}

#[derive(Clone, Copy, serde::Serialize, serde::Deserialize)]
pub struct Lorenz96Parameters<F: NdFloat, S: ForcingSampler<Dtype = F>> {
    pub k: K,
    pub forcing: S,
}
