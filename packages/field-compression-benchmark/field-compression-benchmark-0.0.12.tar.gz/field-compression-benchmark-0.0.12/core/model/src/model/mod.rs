#![cfg_attr(test, allow(clippy::unwrap_used))]

use ndarray::{Array, ArrayView, ArrayViewMut, Dimension, NdFloat};

pub mod any;
pub mod linadv;
pub mod lorenz_63;
pub mod lorenz_96;
pub mod onedsw;
pub mod twodsw;

pub trait Model {
    type Dtype: NdFloat;
    type Dimension: Dimension;
    type State: State<Dtype = Self::Dtype, Dimension = Self::Dimension>;
    type Ext: Clone;

    fn variables(&self) -> impl Iterator<Item = &'static str>;

    fn state(&self) -> <Self::State as State>::View<'_>;
    fn state_mut(&mut self) -> <Self::State as State>::ViewMut<'_>;

    fn tendencies(&self, tendencies: <Self::State as State>::ViewMut<'_>, ext: &mut Self::Ext) {
        self.tendencies_for_state(self.state(), tendencies, ext);
    }

    fn tendencies_for_state(
        &self,
        state: <Self::State as State>::View<'_>,
        tendencies: <Self::State as State>::ViewMut<'_>,
        ext: &mut Self::Ext,
    );

    #[must_use]
    fn with_state(&self, state: Self::State) -> Self
    where
        Self: Sized;
}

pub trait State: Clone {
    type Dtype: NdFloat;
    type Dimension: Dimension;

    type View<'a>: StateView<Dtype = Self::Dtype, Dimension = Self::Dimension, State = Self>
    where
        Self: 'a;
    type ViewMut<'a>: StateViewMut<Dtype = Self::Dtype, Dimension = Self::Dimension, State = Self>
    where
        Self: 'a;

    fn view(&self) -> Self::View<'_>;
    fn view_mut(&mut self) -> Self::ViewMut<'_>;

    fn assign(&mut self, rhs: Self::View<'_>) -> &mut Self {
        self.view_mut().assign(rhs);
        self
    }

    fn add_assign(&mut self, rhs: Self::View<'_>) -> &mut Self {
        self.view_mut().add_assign(rhs);
        self
    }

    fn mul_assign(&mut self, rhs: Self::Dtype) -> &mut Self {
        self.view_mut().mul_assign(rhs);
        self
    }
}

pub trait StateView {
    type Dtype: NdFloat;
    type Dimension: Dimension;

    type State: State<Dtype = Self::Dtype, Dimension = Self::Dimension>;

    fn view(&self) -> <Self::State as State>::View<'_>;
    fn to_owned(&self) -> Self::State;

    fn iter(&self) -> impl Iterator<Item = ArrayView<'_, Self::Dtype, Self::Dimension>> + '_;
}

impl<S: StateView> StateView for &S {
    type Dimension = S::Dimension;
    type Dtype = S::Dtype;
    type State = S::State;

    fn view(&self) -> <Self::State as State>::View<'_> {
        S::view(self)
    }

    fn to_owned(&self) -> Self::State {
        S::to_owned(self)
    }

    fn iter(&self) -> impl Iterator<Item = ArrayView<'_, Self::Dtype, Self::Dimension>> + '_ {
        S::iter(self)
    }
}

pub trait StateViewMut {
    type Dtype: NdFloat;
    type Dimension: Dimension;

    type State: State<Dtype = Self::Dtype, Dimension = Self::Dimension>;

    fn view(&self) -> <Self::State as State>::View<'_>;
    fn view_mut(&mut self) -> <Self::State as State>::ViewMut<'_>;
    fn to_owned(&self) -> Self::State;

    fn iter(&self) -> impl Iterator<Item = ArrayView<'_, Self::Dtype, Self::Dimension>> + '_;
    fn iter_mut(
        &mut self,
    ) -> impl Iterator<Item = ArrayViewMut<'_, Self::Dtype, Self::Dimension>> + '_;

    fn assign(&mut self, rhs: <Self::State as State>::View<'_>) -> &mut Self {
        self.iter_mut()
            .zip(rhs.iter())
            .for_each(|(mut x, rhs)| x.assign(&rhs));
        self
    }

    fn add_assign(&mut self, rhs: <Self::State as State>::View<'_>) -> &mut Self {
        self.iter_mut()
            .zip(rhs.iter())
            .for_each(|(mut x, rhs)| x += &rhs);
        self
    }

    fn mul_assign(&mut self, rhs: Self::Dtype) -> &mut Self {
        self.iter_mut().for_each(|mut x| x *= rhs);
        self
    }
}

impl<S: StateViewMut> StateViewMut for &mut S {
    type Dimension = S::Dimension;
    type Dtype = S::Dtype;
    type State = S::State;

    fn view(&self) -> <Self::State as State>::View<'_> {
        S::view(self)
    }

    fn view_mut(&mut self) -> <Self::State as State>::ViewMut<'_> {
        S::view_mut(self)
    }

    fn to_owned(&self) -> Self::State {
        S::to_owned(self)
    }

    fn iter(&self) -> impl Iterator<Item = ArrayView<'_, Self::Dtype, Self::Dimension>> + '_ {
        S::iter(self)
    }

    fn iter_mut(
        &mut self,
    ) -> impl Iterator<Item = ArrayViewMut<'_, Self::Dtype, Self::Dimension>> + '_ {
        S::iter_mut(self)
    }
}

impl<F: NdFloat, D: Dimension> State for Array<F, D> {
    type Dimension = D;
    type Dtype = F;
    type View<'a>
        = ArrayView<'a, Self::Dtype, Self::Dimension>
    where
        Self: 'a;
    type ViewMut<'a>
        = ArrayViewMut<'a, Self::Dtype, Self::Dimension>
    where
        Self: 'a;

    fn view(&self) -> Self::View<'_> {
        self.view()
    }

    fn view_mut(&mut self) -> Self::ViewMut<'_> {
        self.view_mut()
    }
}

impl<'s, F: NdFloat, D: Dimension> StateView for ArrayView<'s, F, D> {
    type Dimension = D;
    type Dtype = F;
    type State = Array<F, D>;

    fn view(&self) -> <Self::State as State>::View<'_> {
        self.view()
    }

    fn to_owned(&self) -> Self::State {
        self.to_owned()
    }

    fn iter<'a>(
        &'a self,
    ) -> impl Iterator<Item = ArrayView<'a, Self::Dtype, Self::Dimension>> + 'a {
        std::iter::once(self.view())
    }
}

impl<'s, F: NdFloat, D: Dimension> StateViewMut for ArrayViewMut<'s, F, D> {
    type Dimension = D;
    type Dtype = F;
    type State = Array<F, D>;

    fn view(&self) -> <Self::State as State>::View<'_> {
        self.view()
    }

    fn view_mut(&mut self) -> <Self::State as State>::ViewMut<'_> {
        self.view_mut()
    }

    fn to_owned(&self) -> Self::State {
        self.to_owned()
    }

    fn iter<'a>(
        &'a self,
    ) -> impl Iterator<Item = ArrayView<'a, Self::Dtype, Self::Dimension>> + 'a {
        std::iter::once(self.view())
    }

    fn iter_mut<'a>(
        &'a mut self,
    ) -> impl Iterator<Item = ArrayViewMut<'a, Self::Dtype, Self::Dimension>> + 'a {
        std::iter::once(self.view_mut())
    }
}

#[macro_export]
macro_rules! for_each {
    (($ai:pat in $ae:expr $(, $ri:pat in $re:expr)* $(,)?) $code:block) => {
        for_each!(@impl $ae.into_iter() $(, $ri in $re)* => $ai => $code)
    };
    (@impl $ae:expr, $bi:pat in $be:expr $(, $ri:pat in $re:expr)* => $params:pat => $code:block) => {
        for_each!(@impl $ae.zip($be) $(, $ri in $re)* => ($params, $bi) => $code)
    };
    (@impl $ae:expr => $params:pat => $code:block) => {
        #[allow(clippy::reversed_empty_ranges)] // only some ranges are empty
        $ae.for_each(|$params| $code)
    };
}
