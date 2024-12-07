use ndarray::{
    s, Array2, ArrayBase, ArrayView, ArrayViewMut, Ix2, NdFloat, OwnedRepr, RawData, ViewRepr,
};

use crate::{
    boundary::{BoundaryCondition, ZeroBoundary},
    for_each,
    model::{Model, State, StateView, StateViewMut},
    num::two,
};

pub struct TwoDSW<F: NdFloat> {
    parameters: TwoDSWParameters<F>,
    state: TwoDSWState<F, OwnedRepr<F>>,
}

impl<F: NdFloat> TwoDSW<F> {
    #[must_use]
    pub fn new(parameters: TwoDSWParameters<F>) -> Self {
        let TwoDSWParameters { x_dim, y_dim, .. } = parameters;
        Self {
            parameters,
            state: TwoDSWState {
                h_m: Array2::zeros((x_dim, y_dim)),
                u_m_s: Array2::zeros((x_dim, y_dim)),
                v_m_s: Array2::zeros((x_dim, y_dim)),
            },
        }
    }

    #[must_use]
    pub const fn parameters(&self) -> &TwoDSWParameters<F> {
        &self.parameters
    }
}

impl<F: NdFloat> Model for TwoDSW<F> {
    type Dimension = Ix2;
    type Dtype = F;
    type Ext = ();
    type State = TwoDSWState<F, OwnedRepr<F>>;

    fn variables(&self) -> impl Iterator<Item = &'static str> {
        ["h_m", "u_m_s", "v_m_s"].into_iter()
    }

    fn state(&self) -> TwoDSWState<F, ViewRepr<&F>> {
        self.state.view()
    }

    fn state_mut(&mut self) -> TwoDSWState<F, ViewRepr<&mut F>> {
        self.state.view_mut()
    }

    fn tendencies_for_state(
        &self,
        state: TwoDSWState<F, ViewRepr<&F>>,
        mut tendencies: TwoDSWState<F, ViewRepr<&mut F>>,
        _ext: &mut Self::Ext,
    ) {
        let TwoDSWParameters {
            x_dim: _,
            y_dim: _,
            dx_m,
            dy_m,
            f_const_1_s,
            g_const_m_s2,
            nu_const_m2_s,
        } = self.parameters;

        let TwoDSWState { h_m, u_m_s, v_m_s } = state;

        // set the tendency boundary values to zero
        ZeroBoundary::<1>.apply(&mut tendencies);

        let TwoDSWState {
            h_m: mut h_tend_m_s,
            u_m_s: mut u_tend_m_s2,
            v_m_s: mut v_tend_m_s2,
        } = tendencies;

        for_each!((
            dhdt in h_tend_m_s.slice_mut(s![1..-1, 1..-1]),
            dudt in u_tend_m_s2.slice_mut(s![1..-1, 1..-1]),
            dvdt in v_tend_m_s2.slice_mut(s![1..-1, 1..-1]),

            &h_xm1 in h_m.slice(s![..-2, 1..-1]),
            &h_ym1 in h_m.slice(s![1..-1, ..-2]),
            &h in h_m.slice(s![1..-1, 1..-1]),
            &h_xp1 in h_m.slice(s![2.., 1..-1]),
            &h_yp1 in h_m.slice(s![1..-1, 2..]),

            &u_xm1 in u_m_s.slice(s![..-2, 1..-1]),
            &u_ym1 in u_m_s.slice(s![1..-1, ..-2]),
            &u in u_m_s.slice(s![1..-1, 1..-1]),
            &u_xp1 in u_m_s.slice(s![2.., 1..-1]),
            &u_yp1 in u_m_s.slice(s![1..-1, 2..]),

            &v_xm1 in v_m_s.slice(s![..-2, 1..-1]),
            &v_ym1 in v_m_s.slice(s![1..-1, ..-2]),
            &v in v_m_s.slice(s![1..-1, 1..-1]),
            &v_xp1 in v_m_s.slice(s![2.., 1..-1]),
            &v_yp1 in v_m_s.slice(s![1..-1, 2..]),
        ) {
            *dhdt =
                - (u * (h_xp1 - h_xm1) / (dx_m * two()))
                - (v * (h_yp1 - h_ym1) / (dy_m * two()))
                - (h * (
                    ((u_xp1 - u_xm1) / (dx_m * two())) +
                    ((v_yp1 - v_ym1) / (dy_m * two()))
                ));

            *dudt =
                - (u * (u_xp1 - u_xm1) / (dx_m * two()))
                - (v * (u_yp1 - u_ym1) / (dy_m * two()))
                + (f_const_1_s * v)
                - (g_const_m_s2 * (h_xp1 - h_xm1) / (dx_m * two()))
                // diffusion terms
                + (nu_const_m2_s * (u_xm1 - u - u + u_xp1) / (dx_m * dx_m))
                + (nu_const_m2_s * (u_ym1 - u - u + u_yp1) / (dy_m * dy_m));

            *dvdt =
                - (u * (v_xp1 - v_xm1) / (dx_m * two()))
                - (v * (v_yp1 - v_ym1) / (dy_m * two()))
                - (f_const_1_s * u)
                - (g_const_m_s2 * (h_yp1 - h_ym1) / (dy_m * two()))
                // diffusion terms
                + (nu_const_m2_s * (v_xm1 - v - v + v_xp1) / (dx_m * dx_m))
                + (nu_const_m2_s * (v_ym1 - v - v + v_yp1) / (dy_m * dy_m));
        });
    }

    fn with_state(&self, state: TwoDSWState<F, OwnedRepr<F>>) -> Self {
        let mut model = Self::new(self.parameters);
        model.state.h_m.view_mut().assign(&state.h_m);
        model.state.u_m_s.view_mut().assign(&state.u_m_s);
        model.state.v_m_s.view_mut().assign(&state.v_m_s);
        model
    }
}

#[derive(Clone, Copy, serde::Serialize, serde::Deserialize)]
pub struct TwoDSWParameters<F: NdFloat> {
    pub x_dim: usize,
    pub y_dim: usize,
    pub dx_m: F,
    pub dy_m: F,
    pub f_const_1_s: F,
    pub g_const_m_s2: F,
    pub nu_const_m2_s: F,
}

pub struct TwoDSWState<F: NdFloat, S: RawData<Elem = F>> {
    pub h_m: ArrayBase<S, Ix2>,
    pub u_m_s: ArrayBase<S, Ix2>,
    pub v_m_s: ArrayBase<S, Ix2>,
}

impl<F: NdFloat> Clone for TwoDSWState<F, OwnedRepr<F>> {
    fn clone(&self) -> Self {
        Self {
            h_m: self.h_m.clone(),
            u_m_s: self.u_m_s.clone(),
            v_m_s: self.v_m_s.clone(),
        }
    }
}

impl<F: NdFloat> State for TwoDSWState<F, OwnedRepr<F>> {
    type Dimension = Ix2;
    type Dtype = F;
    type View<'a>
        = TwoDSWState<F, ViewRepr<&'a F>>
    where
        Self: 'a;
    type ViewMut<'a>
        = TwoDSWState<F, ViewRepr<&'a mut F>>
    where
        Self: 'a;

    fn view(&self) -> Self::View<'_> {
        TwoDSWState {
            h_m: self.h_m.view(),
            u_m_s: self.u_m_s.view(),
            v_m_s: self.v_m_s.view(),
        }
    }

    fn view_mut(&mut self) -> Self::ViewMut<'_> {
        TwoDSWState {
            h_m: self.h_m.view_mut(),
            u_m_s: self.u_m_s.view_mut(),
            v_m_s: self.v_m_s.view_mut(),
        }
    }
}

impl<'s, F: NdFloat> StateView for TwoDSWState<F, ViewRepr<&'s F>> {
    type Dimension = Ix2;
    type Dtype = F;
    type State = TwoDSWState<F, OwnedRepr<F>>;

    fn view(&self) -> <Self::State as State>::View<'_> {
        TwoDSWState {
            h_m: self.h_m.view(),
            u_m_s: self.u_m_s.view(),
            v_m_s: self.v_m_s.view(),
        }
    }

    fn to_owned(&self) -> Self::State {
        TwoDSWState {
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

impl<'s, F: NdFloat> StateViewMut for TwoDSWState<F, ViewRepr<&'s mut F>> {
    type Dimension = Ix2;
    type Dtype = F;
    type State = TwoDSWState<F, OwnedRepr<F>>;

    fn view(&self) -> <Self::State as State>::View<'_> {
        TwoDSWState {
            h_m: self.h_m.view(),
            u_m_s: self.u_m_s.view(),
            v_m_s: self.v_m_s.view(),
        }
    }

    fn view_mut(&mut self) -> <Self::State as State>::ViewMut<'_> {
        TwoDSWState {
            h_m: self.h_m.view_mut(),
            u_m_s: self.u_m_s.view_mut(),
            v_m_s: self.v_m_s.view_mut(),
        }
    }

    fn to_owned(&self) -> Self::State {
        TwoDSWState {
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
