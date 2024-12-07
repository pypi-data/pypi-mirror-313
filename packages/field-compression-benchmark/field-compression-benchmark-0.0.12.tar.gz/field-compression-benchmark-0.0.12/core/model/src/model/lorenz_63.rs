use ndarray::{Array, ArrayView, ArrayViewMut, Ix1, NdFloat};

use crate::model::Model;

pub struct Lorenz63<F: NdFloat> {
    parameters: Lorenz63Parameters<F>,
    state: [F; 3],
}

impl<F: NdFloat> Lorenz63<F> {
    #[must_use]
    pub fn new(parameters: Lorenz63Parameters<F>) -> Self {
        Self::new_with(parameters, [F::zero(); 3])
    }

    #[must_use]
    pub const fn new_with(parameters: Lorenz63Parameters<F>, state: [F; 3]) -> Self {
        Self { parameters, state }
    }

    #[must_use]
    pub const fn parameters(&self) -> &Lorenz63Parameters<F> {
        &self.parameters
    }
}

impl<F: NdFloat> Model for Lorenz63<F> {
    type Dimension = Ix1;
    type Dtype = F;
    type Ext = ();
    type State = Array<F, Ix1>;

    fn variables(&self) -> impl Iterator<Item = &'static str> {
        ["x123"].into_iter()
    }

    fn state(&self) -> ArrayView<Self::Dtype, Self::Dimension> {
        ArrayView::from(&self.state)
    }

    fn state_mut(&mut self) -> ArrayViewMut<Self::Dtype, Self::Dimension> {
        ArrayViewMut::from(&mut self.state)
    }

    fn tendencies_for_state(
        &self,
        state: ArrayView<Self::Dtype, Self::Dimension>,
        mut tendencies: ArrayViewMut<Self::Dtype, Self::Dimension>,
        _ext: &mut Self::Ext,
    ) {
        let mut new_state = [F::zero(); 3];
        ArrayViewMut::from(&mut new_state).assign(&state);
        let [x1, x2, x3] = new_state;

        let Lorenz63Parameters { sigma, rho, beta } = self.parameters;

        tendencies.assign(&ArrayView::from(&[
            sigma * (x2 - x1),
            x1 * (rho - x3) - x2,
            (x1 * x2) - (beta * x3),
        ]));
    }

    fn with_state(&self, state: Array<Self::Dtype, Self::Dimension>) -> Self {
        let mut model = Self::new(self.parameters);
        ArrayViewMut::from(&mut model.state).assign(&state);
        model
    }
}

#[derive(Clone, Copy, serde::Serialize, serde::Deserialize)]
pub struct Lorenz63Parameters<F: NdFloat> {
    pub sigma: F,
    pub rho: F,
    pub beta: F,
}
