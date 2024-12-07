use ndarray::{
    s, Array1, ArrayBase, ArrayView, ArrayViewMut, Ix1, NdFloat, OwnedRepr, RawData, ViewRepr,
};

use crate::{
    boundary::{BoundaryCondition, ZeroBoundary},
    for_each,
    model::{Model, State, StateView, StateViewMut},
    num::two,
};

pub struct OneDSW<F: NdFloat> {
    parameters: OneDSWParameters<F>,
    state: OneDSWState<F, OwnedRepr<F>>,
}

impl<F: NdFloat> OneDSW<F> {
    #[must_use]
    pub fn new(parameters: OneDSWParameters<F>) -> Self {
        let x_dim = parameters.x_dim;
        Self {
            parameters,
            state: OneDSWState {
                h_m: Array1::zeros((x_dim,)),
                u_m_s: Array1::zeros((x_dim,)),
                v_m_s: Array1::zeros((x_dim,)),
            },
        }
    }

    #[must_use]
    pub const fn parameters(&self) -> &OneDSWParameters<F> {
        &self.parameters
    }
}

impl<F: NdFloat> Model for OneDSW<F> {
    type Dimension = Ix1;
    type Dtype = F;
    type Ext = ();
    type State = OneDSWState<F, OwnedRepr<F>>;

    fn variables(&self) -> impl Iterator<Item = &'static str> {
        ["h_m", "u_m_s", "v_m_s"].into_iter()
    }

    fn state(&self) -> OneDSWState<F, ViewRepr<&F>> {
        self.state.view()
    }

    fn state_mut(&mut self) -> OneDSWState<F, ViewRepr<&mut F>> {
        self.state.view_mut()
    }

    fn tendencies_for_state(
        &self,
        state: OneDSWState<F, ViewRepr<&F>>,
        mut tendencies: OneDSWState<F, ViewRepr<&mut F>>,
        _ext: &mut Self::Ext,
    ) {
        let OneDSWParameters {
            x_dim: _,
            dx_m,
            U_mean_m_s,
            f_const_1_s,
            g_const_m_s2,
            nu_const_m2_s,
        } = self.parameters;

        let OneDSWState { h_m, u_m_s, v_m_s } = state;

        // set the tendency boundary values to zero
        ZeroBoundary::<1>.apply(&mut tendencies);

        let OneDSWState {
            h_m: mut h_tend_m_s,
            u_m_s: mut u_tend_m_s2,
            v_m_s: mut v_tend_m_s2,
        } = tendencies;

        #[expect(non_snake_case)]
        let dH_dy = -U_mean_m_s * f_const_1_s / g_const_m_s2;

        for_each!((
            dhdt in h_tend_m_s.slice_mut(s![1..-1]),
            dudt in u_tend_m_s2.slice_mut(s![1..-1]),
            dvdt in v_tend_m_s2.slice_mut(s![1..-1]),

            &h_m1 in h_m.slice(s![..-2]),
            &h in h_m.slice(s![1..-1]),
            &h_p1 in h_m.slice(s![2..]),

            &u_m1 in u_m_s.slice(s![..-2]),
            &u in u_m_s.slice(s![1..-1]),
            &u_p1 in u_m_s.slice(s![2..]),

            &v_m1 in v_m_s.slice(s![..-2]),
            &v in v_m_s.slice(s![1..-1]),
            &v_p1 in v_m_s.slice(s![2..]),
        ) {
            *dhdt =
                - (u * (h_p1 - h_m1) / (dx_m * two()))
                - (v * dH_dy)
                - (h * (u_p1 - u_m1) / (dx_m * two()));

            *dudt =
                - (u * (u_p1 - u_m1) / (dx_m * two()))
                + (v * f_const_1_s)
                - (g_const_m_s2 * (h_p1 - h_m1) / (dx_m * two()))
                // diffusion term
                + (nu_const_m2_s * (u_m1 - u - u + u_p1) / (dx_m * dx_m));

            *dvdt =
                - (u * (v_p1 - v_m1) / (dx_m * two()))
                - (u * f_const_1_s)
                - (g_const_m_s2 * dH_dy)
                // diffusion term
                + (nu_const_m2_s * (v_m1 - v - v + v_p1) / (dx_m * dx_m));
        });
    }

    fn with_state(&self, state: OneDSWState<F, OwnedRepr<F>>) -> Self {
        let mut model = Self::new(self.parameters);
        model.state.h_m.view_mut().assign(&state.h_m);
        model.state.u_m_s.view_mut().assign(&state.u_m_s);
        model.state.v_m_s.view_mut().assign(&state.v_m_s);
        model
    }
}

#[derive(Clone, Copy, serde::Serialize, serde::Deserialize)]
#[expect(non_snake_case)]
pub struct OneDSWParameters<F: NdFloat> {
    pub x_dim: usize,
    pub dx_m: F,
    pub U_mean_m_s: F,
    pub f_const_1_s: F,
    pub g_const_m_s2: F,
    pub nu_const_m2_s: F,
}

pub struct OneDSWState<F: NdFloat, S: RawData<Elem = F>> {
    pub h_m: ArrayBase<S, Ix1>,
    pub u_m_s: ArrayBase<S, Ix1>,
    pub v_m_s: ArrayBase<S, Ix1>,
}

impl<F: NdFloat> Clone for OneDSWState<F, OwnedRepr<F>> {
    fn clone(&self) -> Self {
        Self {
            h_m: self.h_m.clone(),
            u_m_s: self.u_m_s.clone(),
            v_m_s: self.v_m_s.clone(),
        }
    }
}

impl<F: NdFloat> State for OneDSWState<F, OwnedRepr<F>> {
    type Dimension = Ix1;
    type Dtype = F;
    type View<'a>
        = OneDSWState<F, ViewRepr<&'a F>>
    where
        Self: 'a;
    type ViewMut<'a>
        = OneDSWState<F, ViewRepr<&'a mut F>>
    where
        Self: 'a;

    fn view(&self) -> Self::View<'_> {
        OneDSWState {
            h_m: self.h_m.view(),
            u_m_s: self.u_m_s.view(),
            v_m_s: self.v_m_s.view(),
        }
    }

    fn view_mut(&mut self) -> Self::ViewMut<'_> {
        OneDSWState {
            h_m: self.h_m.view_mut(),
            u_m_s: self.u_m_s.view_mut(),
            v_m_s: self.v_m_s.view_mut(),
        }
    }
}

impl<'s, F: NdFloat> StateView for OneDSWState<F, ViewRepr<&'s F>> {
    type Dimension = Ix1;
    type Dtype = F;
    type State = OneDSWState<F, OwnedRepr<F>>;

    fn view(&self) -> <Self::State as State>::View<'_> {
        OneDSWState {
            h_m: self.h_m.view(),
            u_m_s: self.u_m_s.view(),
            v_m_s: self.v_m_s.view(),
        }
    }

    fn to_owned(&self) -> Self::State {
        OneDSWState {
            h_m: self.h_m.to_owned(),
            u_m_s: self.u_m_s.to_owned(),
            v_m_s: self.v_m_s.to_owned(),
        }
    }

    fn iter<'a>(
        &'a self,
    ) -> impl Iterator<Item = ArrayView<'a, Self::Dtype, Self::Dimension>> + 'a {
        [self.h_m.view(), self.u_m_s.view(), self.v_m_s.view()].into_iter()
    }
}

impl<'s, F: NdFloat> StateViewMut for OneDSWState<F, ViewRepr<&'s mut F>> {
    type Dimension = Ix1;
    type Dtype = F;
    type State = OneDSWState<F, OwnedRepr<F>>;

    fn view(&self) -> <Self::State as State>::View<'_> {
        OneDSWState {
            h_m: self.h_m.view(),
            u_m_s: self.u_m_s.view(),
            v_m_s: self.v_m_s.view(),
        }
    }

    fn view_mut(&mut self) -> <Self::State as State>::ViewMut<'_> {
        OneDSWState {
            h_m: self.h_m.view_mut(),
            u_m_s: self.u_m_s.view_mut(),
            v_m_s: self.v_m_s.view_mut(),
        }
    }

    fn to_owned(&self) -> Self::State {
        OneDSWState {
            h_m: self.h_m.to_owned(),
            u_m_s: self.u_m_s.to_owned(),
            v_m_s: self.v_m_s.to_owned(),
        }
    }

    fn iter<'a>(
        &'a self,
    ) -> impl Iterator<Item = ArrayView<'a, Self::Dtype, Self::Dimension>> + 'a {
        [self.h_m.view(), self.u_m_s.view(), self.v_m_s.view()].into_iter()
    }

    fn iter_mut<'a>(
        &'a mut self,
    ) -> impl Iterator<Item = ArrayViewMut<'a, Self::Dtype, Self::Dimension>> + 'a {
        [
            self.h_m.view_mut(),
            self.u_m_s.view_mut(),
            self.v_m_s.view_mut(),
        ]
        .into_iter()
    }
}
