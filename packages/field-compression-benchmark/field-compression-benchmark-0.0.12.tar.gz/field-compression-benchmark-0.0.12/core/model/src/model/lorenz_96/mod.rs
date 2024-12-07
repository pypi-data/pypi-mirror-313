use std::marker::PhantomData;

use dyn_clone::DynClone;
use ndarray::NdFloat;
use rand::{RngCore, SeedableRng};
use rand_distr::Distribution;

pub mod original;
pub mod wilks_05;

#[derive(
    Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash, serde::Serialize, serde::Deserialize,
)]
#[serde(try_from = "usize", into = "usize")]
pub struct K(usize);

impl K {
    pub const MIN: Self = Self(4);

    #[must_use]
    pub const fn new(x: usize) -> Option<Self> {
        if x >= 4 {
            Some(Self(x))
        } else {
            None
        }
    }

    #[must_use]
    pub const fn get(&self) -> usize {
        self.0
    }
}

impl From<K> for usize {
    fn from(value: K) -> Self {
        value.get()
    }
}

impl TryFrom<usize> for K {
    type Error = &'static str;

    fn try_from(value: usize) -> Result<Self, Self::Error> {
        Self::new(value).ok_or("k must be >= 4")
    }
}

pub trait ForcingSampler: Clone {
    type Dtype: NdFloat;
    type Ext: Clone;

    fn sample(&self, ext: &mut Self::Ext) -> Self::Dtype;
}

#[derive(Clone, Copy, serde::Serialize, serde::Deserialize)]
pub struct Const<F: NdFloat> {
    pub r#const: F,
}

impl<F: NdFloat> Const<F> {
    #[must_use]
    pub const fn new(r#const: F) -> Self {
        Self { r#const }
    }
}

impl<F: NdFloat> ForcingSampler for Const<F> {
    type Dtype = F;
    type Ext = ();

    fn sample(&self, _ext: &mut Self::Ext) -> Self::Dtype {
        self.r#const
    }
}

#[derive(Clone, Copy, serde::Serialize, serde::Deserialize)]
pub struct Distr<F: NdFloat, D: Distribution<F> + Clone> {
    pub distr: D,
    #[serde(skip)]
    _marker: PhantomData<F>,
}

impl<F: NdFloat, D: Distribution<F> + Clone> Distr<F, D> {
    #[must_use]
    pub const fn new(distr: D) -> Self {
        Self {
            distr,
            _marker: PhantomData::<F>,
        }
    }
}

impl<F: NdFloat, D: Distribution<F> + Clone> ForcingSampler for Distr<F, D> {
    type Dtype = F;
    type Ext = AnyRng;

    fn sample(&self, ext: &mut Self::Ext) -> Self::Dtype {
        self.distr.sample(ext)
    }
}

pub struct AnyRng {
    rng: Box<dyn 'static + ClonableRngCore + Send + Sync>,
}

impl AnyRng {
    #[must_use]
    pub fn new(rng: impl 'static + RngCore + SeedableRng + Clone + Send + Sync) -> Self {
        Self { rng: Box::new(rng) }
    }

    pub fn reseed(&mut self) {
        self.rng.reseed();
    }

    pub fn reseed_from_rng(&mut self, rng: &mut impl RngCore) {
        self.rng.reseed_from_rng(rng);
    }
}

impl Clone for AnyRng {
    fn clone(&self) -> Self {
        Self {
            rng: dyn_clone::clone_box(&*self.rng),
        }
    }
}

impl RngCore for AnyRng {
    fn next_u32(&mut self) -> u32 {
        self.rng.next_u32()
    }

    fn next_u64(&mut self) -> u64 {
        self.rng.next_u64()
    }

    fn fill_bytes(&mut self, dest: &mut [u8]) {
        self.rng.fill_bytes(dest);
    }

    fn try_fill_bytes(&mut self, dest: &mut [u8]) -> Result<(), rand::Error> {
        self.rng.try_fill_bytes(dest)
    }
}

trait ClonableRngCore: RngCore + DynClone {
    fn reseed(&mut self);

    fn reseed_from_rng(&mut self, rng: &mut dyn RngCore);
}

impl<T: RngCore + SeedableRng + DynClone> ClonableRngCore for T {
    fn reseed(&mut self) {
        let mut seed = T::Seed::default();
        self.fill_bytes(seed.as_mut());
        *self = T::from_seed(seed);
    }

    fn reseed_from_rng(&mut self, rng: &mut dyn RngCore) {
        let mut seed = T::Seed::default();
        rng.fill_bytes(seed.as_mut());
        *self = T::from_seed(seed);
    }
}
