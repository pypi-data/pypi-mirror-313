use ndarray::{Array, Array1, ArrayView, ArrayViewMut, Ix1, NdFloat};
use rand::{RngCore, SeedableRng};
use rand_distr::{Distribution, Normal, StandardNormal};

use crate::{
    for_each,
    model::{
        lorenz_96::{AnyRng, Distr, K},
        Model,
    },
};

pub struct Lorenz96Wilks05<F: NdFloat>
where
    StandardNormal: Distribution<F>,
{
    parameters: Lorenz96Wilks05Parameters<F>,
    state: Array1<F>,
}

impl<F: NdFloat> Lorenz96Wilks05<F>
where
    StandardNormal: Distribution<F>,
{
    #[must_use]
    pub fn new(parameters: Lorenz96Wilks05Parameters<F>) -> Self {
        let k = parameters.k;
        Self {
            parameters,
            state: Array1::zeros((k.get(),)),
        }
    }

    #[must_use]
    pub const fn parameters(&self) -> &Lorenz96Wilks05Parameters<F> {
        &self.parameters
    }
}

impl<F: NdFloat> Model for Lorenz96Wilks05<F>
where
    StandardNormal: Distribution<F>,
{
    type Dimension = Ix1;
    type Dtype = F;
    type Ext = EtaWithAnyRng<F>;
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
        let Lorenz96Wilks05Parameters {
            k: _,
            forcing,
            forcing_lag,
            subgrid_fit,
        } = &self.parameters;

        for_each!((
            dxdt in tendencies,

            &x_m2 in state.iter().cycle().skip(state.len() - 2),
            &x_m1 in state.iter().cycle().skip(state.len() - 1),
            &x in state.iter(),
            &x_p1 in state.iter().cycle().skip(1),

            &eta in ext.eta(),
        ) {
            let subgrid_fit = subgrid_fit.iter().scan(F::one(), |x_pow_i, &b_i| {
                let term_i = *x_pow_i * b_i;
                *x_pow_i *= x;
                Some(term_i)
            }).fold(F::zero(), |sum, term_i| sum + term_i);

            *dxdt = -x_m2 * x_m1 + x_m1 * x_p1 - x + forcing.distr.mean() - subgrid_fit
                + eta;
        });

        ext.update(&forcing.distr, *forcing_lag);
    }

    fn with_state(&self, state: Array<Self::Dtype, Self::Dimension>) -> Self {
        let mut model = Self::new(self.parameters.clone());
        model.state.view_mut().assign(&state);
        model
    }
}

#[derive(Clone, serde::Serialize, serde::Deserialize)]
pub struct Lorenz96Wilks05Parameters<F: NdFloat>
where
    StandardNormal: Distribution<F>,
{
    pub k: K,
    pub forcing: Distr<F, Normal<F>>,
    pub forcing_lag: ClosedUnit<F>,
    pub subgrid_fit: Vec<F>,
}

#[derive(Clone)]
pub struct EtaWithAnyRng<F: NdFloat>
where
    StandardNormal: Distribution<F>,
{
    eta: Array<F, Ix1>,
    rng: AnyRng,
}

impl<F: NdFloat> EtaWithAnyRng<F>
where
    StandardNormal: Distribution<F>,
{
    pub fn zeros(k: K, rng: impl 'static + RngCore + SeedableRng + Clone + Send + Sync) -> Self {
        Self {
            eta: Array1::zeros((k.get(),)),
            rng: AnyRng::new(rng),
        }
    }

    pub fn update(&mut self, forcing: &Normal<F>, forcing_lag: ClosedUnit<F>) {
        for eta_k in &mut self.eta {
            *eta_k = forcing_lag.get() * (*eta_k)
                + forcing.std_dev()
                    * forcing_lag.sq().one_minus().sqrt().get()
                    * StandardNormal.sample(&mut self.rng);
        }
    }

    #[must_use]
    pub fn eta(&self) -> ArrayView<F, Ix1> {
        self.eta.view()
    }

    #[must_use]
    pub fn rng(&mut self) -> &mut AnyRng {
        &mut self.rng
    }
}

#[derive(Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub struct ClosedUnit<F: NdFloat>(F);

impl<F: NdFloat> ClosedUnit<F> {
    pub fn new(value: F) -> Option<Self> {
        if value >= F::zero() && value <= F::one() {
            Some(Self(value))
        } else {
            None
        }
    }

    #[must_use]
    pub const fn get(self) -> F {
        self.0
    }

    #[must_use]
    pub fn one_minus(self) -> Self {
        Self(F::one() - self.0)
    }

    #[must_use]
    pub fn sq(self) -> Self {
        Self(self.0 * self.0)
    }

    #[must_use]
    pub fn sqrt(self) -> Self {
        Self(self.0.sqrt())
    }

    #[must_use]
    pub fn zero() -> Self {
        Self(F::zero())
    }

    #[must_use]
    pub fn one() -> Self {
        Self(F::one())
    }
}

impl<F: NdFloat + serde::Serialize> serde::Serialize for ClosedUnit<F> {
    fn serialize<S: serde::Serializer>(&self, serializer: S) -> Result<S::Ok, S::Error> {
        self.0.serialize(serializer)
    }
}

impl<'de, F: NdFloat + serde::Deserialize<'de>> serde::Deserialize<'de> for ClosedUnit<F> {
    fn deserialize<D: serde::Deserializer<'de>>(deserializer: D) -> Result<Self, D::Error> {
        Self::new(F::deserialize(deserializer)?)
            .ok_or_else(|| serde::de::Error::custom("value must be in 0.0 <= x <= 1.0"))
    }
}

#[cfg(test)]
mod tests {
    use std::marker::PhantomData;

    use num_traits::Float;
    use rand::SeedableRng;
    use rand_distr::Normal;

    use crate::{
        boundary::NoopBoundary,
        model::{
            lorenz_96::{
                original::{Lorenz96, Lorenz96Parameters},
                wilks_05::{ClosedUnit, EtaWithAnyRng, Lorenz96Wilks05, Lorenz96Wilks05Parameters},
                AnyRng, Const, Distr, K,
            },
            Model,
        },
        stepping::{RungeKutta4, TimeStepping},
    };

    #[test]
    fn const_forcing() {
        let mut original = Lorenz96::new(Lorenz96Parameters {
            k: K::new(36).unwrap(),
            forcing: Const { r#const: 8.0 },
        });
        let mut original_ext = ();
        let mut original_extrapolation = RungeKutta4::new(&original);

        let mut wilks05 = Lorenz96Wilks05::new(Lorenz96Wilks05Parameters {
            k: K::new(36).unwrap(),
            forcing: Distr {
                distr: Normal::new(8.0, 0.0).unwrap(),
                _marker: PhantomData,
            },
            forcing_lag: ClosedUnit::zero(),
            subgrid_fit: vec![],
        });
        let mut wilks05_ext =
            EtaWithAnyRng::zeros(K::new(36).unwrap(), rand::rngs::StdRng::seed_from_u64(42));
        let mut wilks05_boundary = NoopBoundary;
        let mut wilks05_extrapolation = RungeKutta4::new(&wilks05);

        for _ in 0..1_000 {
            original_extrapolation.step(
                &mut original,
                &mut original_ext,
                &mut wilks05_boundary,
                0.003,
            );
            wilks05_extrapolation.step(
                &mut wilks05,
                &mut wilks05_ext,
                &mut wilks05_boundary,
                0.003,
            );

            assert_eq!(original.state(), wilks05.state());
        }
    }

    #[test]
    fn const_forcing_with_lag() {
        let mut original = Lorenz96::new(Lorenz96Parameters {
            k: K::new(36).unwrap(),
            forcing: Const { r#const: 8.0 },
        });
        let mut original_ext = ();
        let mut original_extrapolation = RungeKutta4::new(&original);

        let mut wilks05 = Lorenz96Wilks05::new(Lorenz96Wilks05Parameters {
            k: K::new(36).unwrap(),
            forcing: Distr {
                distr: Normal::new(8.0, 1.0).unwrap(),
                _marker: PhantomData,
            },
            forcing_lag: ClosedUnit::one(),
            subgrid_fit: vec![],
        });
        let mut wilks05_ext =
            EtaWithAnyRng::zeros(K::new(36).unwrap(), rand::rngs::StdRng::seed_from_u64(42));
        let mut wilks05_boundary = NoopBoundary;
        let mut wilks05_extrapolation = RungeKutta4::new(&wilks05);

        for _ in 0..1_000 {
            original_extrapolation.step(
                &mut original,
                &mut original_ext,
                &mut wilks05_boundary,
                0.003,
            );
            wilks05_extrapolation.step(
                &mut wilks05,
                &mut wilks05_ext,
                &mut wilks05_boundary,
                0.003,
            );

            assert_eq!(original.state(), wilks05.state());
        }
    }

    #[test]
    fn stochastic_forcing() {
        let mut original = Lorenz96::new(Lorenz96Parameters {
            k: K::new(36).unwrap(),
            forcing: Distr {
                distr: Normal::new(8.0, 1.0).unwrap(),
                _marker: PhantomData,
            },
        });
        let mut original_ext = AnyRng::new(rand::rngs::StdRng::seed_from_u64(42));
        let mut original_extrapolation = RungeKutta4::new(&original);

        let mut wilks05 = Lorenz96Wilks05::new(Lorenz96Wilks05Parameters {
            k: K::new(36).unwrap(),
            forcing: Distr {
                distr: Normal::new(8.0, 1.0).unwrap(),
                _marker: PhantomData,
            },
            forcing_lag: ClosedUnit::zero(),
            subgrid_fit: vec![],
        });
        let mut wilks05_ext =
            EtaWithAnyRng::zeros(K::new(36).unwrap(), rand::rngs::StdRng::seed_from_u64(42));
        wilks05_ext.update(
            &wilks05.parameters().forcing.distr,
            wilks05.parameters().forcing_lag,
        );
        let mut wilks05_boundary = NoopBoundary;
        let mut wilks05_extrapolation = RungeKutta4::new(&wilks05);

        for _ in 0..1_000 {
            original_extrapolation.step(
                &mut original,
                &mut original_ext,
                &mut wilks05_boundary,
                0.003,
            );
            wilks05_extrapolation.step(
                &mut wilks05,
                &mut wilks05_ext,
                &mut wilks05_boundary,
                0.003,
            );

            let abs_err: f64 =
                (original.state().to_owned() - wilks05.state()).fold(0.0, |a, b| b.abs().max(a));

            assert!(abs_err < 1e-12);

            // ensure that rounding errors don't fail the test
            wilks05.state_mut().assign(&original.state());
        }
    }
}
