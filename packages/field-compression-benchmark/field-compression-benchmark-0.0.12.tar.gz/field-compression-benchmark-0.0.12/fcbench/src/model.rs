use pyo3::{intern, prelude::*, sync::GILOnceCell, types::PyTuple};

use crate::dataclass::{Dataclass, DataclassRegistry};

/// Create a [`PyModule`] with name "model" that exports the [`Model`],
/// [`TimeStepping`], and [`Boundary`].
///
/// The created module is expected to be a submodule of `fcbench` since the
/// all exports expect to have the `fcbench.model` module path.
pub fn create_module(py: Python) -> Result<Bound<PyModule>, PyErr> {
    let module = PyModule::new(py, "model")?;

    module.add_class::<Model>()?;
    module.add_class::<TimeStepping>()?;
    module.add_class::<Boundary>()?;

    let types = PyModule::new(py, "types")?;
    dataclass_registry().export(py, types.as_borrowed())?;
    module.add_submodule(&types)?;

    Ok(module)
}

fn dataclass_registry() -> DataclassRegistry {
    let mut registry = DataclassRegistry::new();

    registry.insert::<core_model::model::lorenz_63::Lorenz63Parameters<f64>>();
    registry.insert_with_sample(
        &core_model::model::lorenz_96::original::Lorenz96Parameters {
            k: core_model::model::lorenz_96::K::MIN,
            forcing: Lorenz96Forcing::Const(core_model::model::lorenz_96::Const::new(0.0)),
        },
    );
    registry.insert_with_sample(
        &core_model::model::lorenz_96::original::Lorenz96Parameters {
            k: core_model::model::lorenz_96::K::MIN,
            forcing: Lorenz96Forcing::Distr(core_model::model::lorenz_96::Distr::new(
                standard_normal(),
            )),
        },
    );
    registry.insert_with_sample(
        &core_model::model::lorenz_96::wilks_05::Lorenz96Wilks05Parameters {
            k: core_model::model::lorenz_96::K::MIN,
            forcing: core_model::model::lorenz_96::Distr::new(standard_normal()),
            forcing_lag: core_model::model::lorenz_96::wilks_05::ClosedUnit::zero(),
            subgrid_fit: vec![2.0, 0.1],
        },
    );
    registry.insert::<core_model::model::linadv::LinadvParameters<f64>>();
    registry.insert::<core_model::model::onedsw::OneDSWParameters<f64>>();
    registry.insert::<core_model::model::twodsw::TwoDSWParameters<f64>>();

    registry
}

#[expect(clippy::unwrap_used)] // FIXME
fn standard_normal() -> rand_distr::Normal<f64> {
    rand_distr::Normal::new(0.0, 1.0).unwrap()
}

#[pyclass(module = "fcbench.model")]
/// A generalised multi-variable and multi-dimensional numerical model that
/// provides mutable views into its state as the model is advanced each step.
///
/// Use one of the following constructors to create a new
/// Shallow-Water-[`Model`]:
///
/// - [`Model::linadv`] creates a 1D Linear Advection model
/// - [`Model::onedsw`] creates a 1D Shallow-Water model
/// - [`Model::twodsw`] creates a 2D Shallow-Water model
///
/// Use one of the following constructors to create a new Lorenz-[`Model`]:
///
/// - [`Model::lorenz_63`] creates a Lorenz'63 model
/// - [`Model::lorenz_96_with_const_forcing`] creates a basic Lorenz'96 model
///   with constant forcing
/// - [`Model::lorenz_96_with_stochastic_forcing`] creates a basic Lorenz'96
///   model with normal-distributed forcing
/// - [`Model::lorenz_96_with_wilks_05_parameterisation`] creates Lorenz'96
///   model using the Wilks'05 parameterisation of subgrid-scale processes.
///
/// After creation, use the [`Model::state`] accessor to read or modify the
/// model's inner state, and [`Model::step`] to advance the model by a single
/// timestep.
///
/// Note that the model can also be iterated over to produce a stream of model
/// states:
///
/// ```python
/// # Create a 1D Linear Advection Shallow-Water model
/// model = Model.linadv(
///     params=dict(x_dim=99, dx_m: 10_000, U_const_m_s=10),
///     stepping=TimeStepping.Heun,
///     boundary=Boundary.Periodic,
///     dt=300,
/// )
/// initialise_model_state(model.state)
///
/// # Iterate over the advancing model's states
/// for state in model:
///     inspect_model_state(state)
/// ```
pub struct Model {
    model: core_model::model::any::AnyModel<f64>,
    ext: core_model::model::any::AnyExt,
    stepping: core_model::stepping::AnyTimeStepping<f64>,
    boundary: core_model::boundary::AnyBoundary<f64>,
    dt: f64,
}

#[pymethods]
impl Model {
    #[getter]
    /// A mutable view into the current model state.
    ///
    /// The model state is represented by a [`namedtuple`] such that state
    /// variables can be accessed either by name or by iterating over the
    /// state. Each state variable is a mutable view into a [`numpy.array`].
    ///
    /// [`namedtuple`]: https://docs.python.org/3.10/library/collections.html#collections.namedtuple
    /// [`numpy.array`]: https://numpy.org/doc/1.26/reference/generated/numpy.array.html
    ///
    /// [SIGNATURE]: # "(self) -> NamedTuple('State', **Mapping[str, numpy.array])"
    pub fn state<'py>(this: &Bound<'py, Self>) -> Result<Bound<'py, PyAny>, PyErr> {
        static NAMEDTUPLE: GILOnceCell<Py<PyAny>> = GILOnceCell::new();

        let py: Python = (*this).py();

        let mut slf: PyRefMut<Self> = this.try_borrow_mut()?;
        let slf: &mut Self = &mut slf;

        let namedtuple = NAMEDTUPLE.import(py, "collections", "namedtuple")?.call1((
            intern!(py, "State"),
            PyTuple::new(
                py,
                #[expect(clippy::needless_collect)]
                core_model::model::Model::variables(&slf.model).collect::<Vec<_>>(),
            )?,
        ))?;

        let mut state = core_model::model::Model::state_mut(&mut slf.model);

        namedtuple.call1(PyTuple::new(
            py,
            #[expect(clippy::needless_collect)]
            core_model::model::StateViewMut::iter_mut(&mut state)
                .map(|state| {
                    // SAFETY: The memory backing `state` will stay valid as long as this
                    //         object is alive, as we do not modify `state` in any way
                    //         which would cause it to be reallocated.
                    #[expect(unsafe_code)]
                    unsafe {
                        numpy::PyArrayDyn::borrow_from_array(&state, this.as_any().clone())
                    }
                })
                .collect::<Vec<_>>(),
        )?)
    }

    /// Advance the model by a single timestep.
    ///
    /// If `dt` is `None`, the model's default timestep `$\Delta t$` is used.
    /// Otherwise, the model is advanced by the given timestep `$\Delta t$`.
    ///
    /// [SIGNATURE]: # "(self, /, dt: Optional[float] = None)"
    #[pyo3(signature = (dt=None))]
    pub fn step(&mut self, dt: Option<f64>) {
        core_model::stepping::TimeStepping::step(
            &mut self.stepping,
            &mut self.model,
            &mut self.ext,
            &mut self.boundary,
            dt.unwrap_or(self.dt),
        );
    }

    #[getter]
    /// The default timestep `$\Delta t$` that the model uses to advance.
    ///
    /// [SIGNATURE]: # "(self) -> float"
    #[must_use]
    pub const fn dt(&self) -> f64 {
        self.dt
    }

    /// Create a deep copy of the model.
    ///
    /// [SIGNATURE]: # "(self) -> Model"
    #[must_use]
    pub fn deepcopy(&self) -> Self {
        Clone::clone(self)
    }

    /// Create an ensemble from this model.
    ///
    /// Note that the original model is not modified and is not part of the
    /// returned model ensemble.
    #[must_use]
    pub fn ensemble(&self, size: usize) -> Vec<Self> {
        // TODO: provide some kind of generic access to the rng
        macro_rules! provide_model_rng {
            ($model:ident) => {
                if let Some(rng) = $model
                    .ext
                    .downcast_mut::<core_model::model::lorenz_96::AnyRng>()
                {
                    Some(rng)
                } else if let Some(eta) = $model
                    .ext
                    .downcast_mut::<core_model::model::lorenz_96::wilks_05::EtaWithAnyRng<f64>>(
                ) {
                    Some(eta.rng())
                } else {
                    None
                }
            };
        }

        let mut ensemble = (0..size).map(|_| self.deepcopy()).collect::<Vec<_>>();

        let [first, rest @ ..] = ensemble.as_mut_slice() else {
            return ensemble;
        };
        let Some(rng) = provide_model_rng!(first) else {
            return ensemble;
        };

        for model in rest {
            if let Some(model_rng) = provide_model_rng!(model) {
                model_rng.reseed_from_rng(rng);
            }
        }
        rng.reseed();

        ensemble
    }

    /// Use the model as a stream to iterate over the future timesteps.
    ///
    /// Each iteration of the returned iterator advances the model by a single
    /// timestep using the model's default timestep `$\Delta t$`.
    ///
    /// This method can be used to pull the next model states out of the
    /// advancing model in a for loop.
    #[must_use]
    pub const fn __iter__(this: PyRef<Self>) -> PyRef<Self> {
        this
    }

    /// Advance the model by a single timestep using the model's default
    /// timestep `$\Delta t$`. This method returns a mutable view into the
    /// model's new state.
    ///
    /// Please see [`Model::step`] for a more explicit model step method and
    /// [`Model::state`] for a more explicit model state accessor.
    pub fn __next__<'py>(this: &Bound<'py, Self>) -> Result<Option<Bound<'py, PyAny>>, PyErr> {
        {
            let mut slf: PyRefMut<Self> = this.try_borrow_mut()?;
            let slf: &mut Self = &mut slf;

            slf.step(None);
        }

        Self::state(this).map(Some)
    }

    #[staticmethod]
    #[expect(clippy::needless_pass_by_value)]
    /// Creates a Lorenz'63 model with `params`, a time `stepping` scheme,
    /// and the timestep `$\Delta t$` `dt`.
    ///
    /// The Lorenz'63 model [^1] is described by the following sytem of
    /// equations:
    ///
    /// ```math
    /// \begin{align}
    ///     \dot{x_1} &= \sigma ( x_2 - x_1 ) \newline
    ///     \dot{x_2} &= x_1 ( \rho - x_3 ) - x_2 \newline
    ///     \dot{x_3} &= x_1 x_2 - \beta x_3
    /// \end{align}
    /// ```
    ///
    /// The model's state has one variable, `x123`, which is of shape `$(3,)$`.
    ///
    /// [^1]:
    ///   Baines, P. G. (2008). Lorenz, E.N. (1963). Deterministic nonperiodic
    ///   flow. Journal of the Atmospheric Sciences 20, 130–141. *Progress in
    ///   Physical Geography: Earth and Environment*, 32(4), 475-480. Available
    ///   from: <https://doi.org/10.1177/0309133308091948>.
    ///
    /// [SIGNATURE]: # "(params: types.Lorenz63Parameters, stepping: TimeStepping, dt: float) -> Model"
    #[must_use]
    pub fn lorenz_63(
        params: Dataclass<core_model::model::lorenz_63::Lorenz63Parameters<f64>>,
        stepping: &TimeStepping,
        dt: f64,
    ) -> Self {
        let (model, ext) = core_model::model::any::AnyModel::new(
            core_model::model::lorenz_63::Lorenz63::new(*params),
            Box::new(()),
        );
        let stepping = stepping.as_any(&model);

        Self {
            model,
            ext,
            stepping,
            boundary: core_model::boundary::AnyBoundary::new(core_model::boundary::NoopBoundary),
            dt,
        }
    }

    #[staticmethod]
    #[expect(clippy::needless_pass_by_value)]
    /// Creates a Lorenz'96 model with `params`, a time `stepping` scheme,
    /// and the timestep `$\Delta t$` `dt`.
    ///
    /// The model's forcing `$F$` is constant.
    ///
    /// The basic Lorenz'96 model [^2] is described by the following equation:
    ///
    /// ```math
    /// \begin{align}
    ///     \frac{\partial X_k}{\partial t} &= -X_{k-2} \cdot X_{k-1} + X_{k-1}
    ///     \cdot X_{k+1} - X_{k} + F
    /// \end{align}
    /// ```
    ///
    /// The model's state has one variable, `X_k`, which is of shape `$(k,)$`.
    ///
    /// [^2]:
    ///   Lorenz, E.N. (1995). Predictability: a problem partly solved.
    ///   *Seminar on Predictability, 4-8 September 1995*. ECMWF. Available
    ///   from: <https://www.ecmwf.int/en/elibrary/75462-predictability-problem-partly-solved>
    ///   [Accessed: 18th March 2024].
    ///
    /// [SIGNATURE]: # "(params: types.Lorenz96Parameters, stepping: TimeStepping, dt: float) -> Model"
    #[must_use]
    pub fn lorenz_96_with_const_forcing(
        params: Dataclass<
            core_model::model::lorenz_96::original::Lorenz96Parameters<
                f64,
                core_model::model::lorenz_96::Const<f64>,
            >,
        >,
        stepping: &TimeStepping,
        dt: f64,
    ) -> Self {
        let (model, ext) = core_model::model::any::AnyModel::new(
            core_model::model::lorenz_96::original::Lorenz96::new(*params),
            Box::new(()),
        );
        let stepping = stepping.as_any(&model);

        Self {
            model,
            ext,
            stepping,
            boundary: core_model::boundary::AnyBoundary::new(core_model::boundary::NoopBoundary),
            dt,
        }
    }

    #[staticmethod]
    #[expect(clippy::needless_pass_by_value)]
    /// Creates a Lorenz'96 model with `params`, a time `stepping` scheme,
    /// the timestep `$\Delta t$` `dt`, and a random number generator with
    /// `seed`.
    ///
    /// The model's forcing `$F$` is  drawn from a normal distribution
    /// `$F \sim \text{N}(\mu, {\sigma}^2)$` on each model step.
    ///
    /// The basic Lorenz'96 model [^3] is described by the following equation:
    ///
    /// ```math
    /// \begin{align}
    ///     \frac{\partial X_k}{\partial t} &= -X_{k-2} \cdot X_{k-1} + X_{k-1}
    ///     \cdot X_{k+1} - X_{k} + F
    /// \end{align}
    /// ```
    ///
    /// The model's state has one variable, `X_k`, which is of shape `$(k,)$`.
    ///
    /// [^3]:
    ///   Lorenz, E.N. (1995). Predictability: a problem partly solved.
    ///   *Seminar on Predictability, 4-8 September 1995*. ECMWF. Available
    ///   from: <https://www.ecmwf.int/en/elibrary/75462-predictability-problem-partly-solved>
    ///   [Accessed: 18th March 2024].
    ///
    /// [SIGNATURE]: # "(params: types.Lorenz96Parameters, stepping: TimeStepping, dt: float, seed: int) -> Model"
    #[must_use]
    pub fn lorenz_96_with_stochastic_forcing(
        params: Dataclass<
            core_model::model::lorenz_96::original::Lorenz96Parameters<
                f64,
                core_model::model::lorenz_96::Distr<f64, rand_distr::Normal<f64>>,
            >,
        >,
        stepping: &TimeStepping,
        dt: f64,
        seed: u64,
    ) -> Self {
        let (model, ext) = core_model::model::any::AnyModel::new(
            core_model::model::lorenz_96::original::Lorenz96::new(*params),
            Box::new(core_model::model::lorenz_96::AnyRng::new(
                <rand_chacha::ChaChaRng as rand_chacha::rand_core::SeedableRng>::seed_from_u64(
                    seed,
                ),
            )),
        );
        let stepping = stepping.as_any(&model);

        Self {
            model,
            ext,
            stepping,
            boundary: core_model::boundary::AnyBoundary::new(core_model::boundary::NoopBoundary),
            dt,
        }
    }

    #[staticmethod]
    #[expect(clippy::needless_pass_by_value)]
    /// Creates a Lorenz'96 model with the Wilks (2005) parameterisation with
    /// `params`, a time `stepping` scheme, the timestep `$\Delta t$`
    /// `dt`, and a random number generator with `seed`.
    ///
    /// The model's forcing `$F$` is  drawn from a normal distribution
    /// `$F \sim \text{N}(\mu, {\sigma}^2)$` with lag-1 auto-correlation
    /// on each model step.
    ///
    /// The parameterised Lorenz'96 model [^4] is described by the following
    /// equations:
    ///
    /// ```math
    /// \begin{align}
    ///     \frac{\partial X_k}{\partial t} &= -X_{k-2} \cdot X_{k-1} + X_{k-1}
    ///     \cdot X_{k+1} - X_{k} + F - g_{U}(X_{k}) + e_{k} \newline
    ///     g_{U}(X_{k}) &= \sum_{i=0}^{B-1} b_{i} \cdot
    ///     {\left( X_{k} \right)}^{i} \newline
    ///     e_{k}(t + \Delta t) &= \phi e_{k}(t) + \sigma_{e} \cdot
    ///     \sqrt{1-{\phi}^{2}} \cdot z_{k}(t)
    /// \end{align}
    /// ```
    ///
    /// where `$z_{k} \sim \text{N}(0, 1^2)$`.
    ///
    /// The model's state has one variable, `X_k`, which is of shape `$(k,)$`.
    ///
    /// [^4]:
    ///   Wilks, D.S. (2005). Effects of stochastic parametrizations in the
    ///   Lorenz '96 system. *Q.J.R. Meteorol. Soc.*, 131:389-407. Available
    ///   from: <https://doi.org/10.1256/qj.04.03>.
    ///
    /// [SIGNATURE]: # "(params: types.Lorenz96Wilks05Parameters, stepping: TimeStepping, dt: float, seed: int) -> Model"
    #[must_use]
    pub fn lorenz_96_with_wilks_05_parameterisation(
        params: Dataclass<core_model::model::lorenz_96::wilks_05::Lorenz96Wilks05Parameters<f64>>,
        stepping: &TimeStepping,
        dt: f64,
        seed: u64,
    ) -> Self {
        let mut eta = core_model::model::lorenz_96::wilks_05::EtaWithAnyRng::zeros(
            params.k,
            <rand_chacha::ChaChaRng as rand_chacha::rand_core::SeedableRng>::seed_from_u64(seed),
        );
        eta.update(&params.forcing.distr, params.forcing_lag);

        let (model, ext) = core_model::model::any::AnyModel::new(
            core_model::model::lorenz_96::wilks_05::Lorenz96Wilks05::new((*params).clone()),
            Box::new(eta),
        );
        let stepping = stepping.as_any(&model);

        Self {
            model,
            ext,
            stepping,
            boundary: core_model::boundary::AnyBoundary::new(core_model::boundary::NoopBoundary),
            dt,
        }
    }

    #[staticmethod]
    #[expect(clippy::needless_pass_by_value)]
    /// Creates a 1D (Only-)Linear Advection Shallow-Water model with `params`,
    /// a time `stepping` scheme, a `boundary` condition, and the timestep
    /// `$\Delta t$` `dt`.
    ///
    /// The 1D Linear Advection model is described by the following equation:
    ///
    /// ```math
    /// \begin{align}
    ///     \frac{\partial h}{\partial t} &=
    ///         -\overline{U} \frac{\partial h}{\partial x}
    /// \end{align}
    /// ```
    ///
    /// where `$\overline{U} = \text{const}$` and
    /// `$\frac{\partial h}{\partial x}$` is computed for grid cell `$i$`
    /// using the centered difference approximation:
    ///
    /// ```math
    /// \begin{align}
    ///     { \left( \frac{\partial h}{\partial x} \right) }_{i} &=
    ///         \frac{h_{i+1} - h_{i-1}}{2 \Delta x}
    /// \end{align}
    /// ```
    ///
    /// The model's state has one variable, `h`, which is of shape
    /// `$(x_{dim},)$`.
    ///
    /// [SIGNATURE]: # "(params: types.LinadvParameters, stepping: TimeStepping, boundary: Boundary, dt: float) -> Model"
    #[must_use]
    pub fn linadv(
        params: Dataclass<core_model::model::linadv::LinadvParameters<f64>>,
        stepping: &TimeStepping,
        boundary: &Boundary,
        dt: f64,
    ) -> Self {
        let (model, ext) = core_model::model::any::AnyModel::new(
            core_model::model::linadv::Linadv::new(*params),
            Box::new(()),
        );
        let stepping = stepping.as_any(&model);
        let boundary = boundary.as_any();

        Self {
            model,
            ext,
            stepping,
            boundary,
            dt,
        }
    }

    #[staticmethod]
    #[expect(clippy::needless_pass_by_value)]
    /// Creates a 1D (non-linear advection) Shallow-Water model with `params`,
    /// a time `stepping` scheme, a `boundary` condition, and the timestep
    /// `$\Delta t$` `dt`.
    ///
    /// The 1D shallow water model is described by the following system of
    /// equations:
    ///
    /// ```math
    /// \begin{align}
    ///     \frac{\partial h}{\partial t} &=
    ///         - u \cdot \frac{\partial h}{\partial x}
    ///         - v \cdot \frac{\partial H}{\partial y}
    ///         - h \cdot \frac{\partial u}{\partial x} \newline
    ///     \frac{\partial u}{\partial t} &=
    ///         - u \cdot \frac{\partial u}{\partial x}
    ///         + f \cdot v
    ///         - g \cdot \frac{\partial h}{\partial x} \newline
    ///     \frac{\partial v}{\partial t} &=
    ///         - u \cdot \frac{\partial v}{\partial x}
    ///         - f \cdot u
    ///         - g \cdot \frac{\partial H}{\partial y}
    /// \end{align}
    /// ```
    ///
    /// where `$\frac{\partial H}{\partial y} = -\frac{f}{g} \cdot \overline{U}
    /// = \text{const}$` and `$\frac{\partial F}{\partial x}$` for any
    /// `$F \in \{ h, u, v \}$` is computed for grid cell `$i$` using the
    /// centered difference approximation:
    ///
    /// ```math
    /// \begin{align}
    ///     { \left( \frac{\partial F}{\partial x} \right) }_{i} &=
    ///         \frac{F_{i+1} - F_{i-1}}{2 \Delta x}
    /// \end{align}
    /// ```
    ///
    /// The model's state has three variables, `h`, `u`, and `v`, which are of
    /// shape `$(x_{dim},)$`.
    ///
    /// [SIGNATURE]: # "(params: types.OneDSWParameters, stepping: TimeStepping, boundary: Boundary, dt: float) -> Model"
    #[must_use]
    pub fn onedsw(
        params: Dataclass<core_model::model::onedsw::OneDSWParameters<f64>>,
        stepping: &TimeStepping,
        boundary: &Boundary,
        dt: f64,
    ) -> Self {
        let (model, ext) = core_model::model::any::AnyModel::new(
            core_model::model::onedsw::OneDSW::new(*params),
            Box::new(()),
        );
        let stepping = stepping.as_any(&model);
        let boundary = boundary.as_any();

        Self {
            model,
            ext,
            stepping,
            boundary,
            dt,
        }
    }

    #[staticmethod]
    #[expect(clippy::needless_pass_by_value)]
    /// Creates a 2D (non-linear advection) Shallow-Water model with `params`,
    /// a time `stepping` scheme, a `boundary` condition, and the timestep
    /// `$\Delta t$` `dt`.
    ///
    /// The 2D shallow water model is described by the following system of
    /// equations:
    ///
    /// ```math
    /// \begin{align}
    ///     \frac{\partial h}{\partial t} &=
    ///         - u \cdot \frac{\partial h}{\partial x}
    ///         - v \cdot \frac{\partial h}{\partial y}
    ///         - h \cdot \left( \frac{\partial u}{\partial x} + \frac{\partial
    ///           v}{\partial y}
    ///         \right) \newline
    ///     \frac{\partial u}{\partial t} &=
    ///         - u \cdot \frac{\partial u}{\partial x}
    ///         - v \cdot \frac{\partial u}{\partial y}
    ///         + f \cdot v
    ///         - g \cdot \frac{\partial h}{\partial x} \newline
    ///     \frac{\partial v}{\partial t} &=
    ///         - u \cdot \frac{\partial v}{\partial x}
    ///         - v \cdot \frac{\partial v}{\partial y}
    ///         - f \cdot u
    ///         - g \cdot \frac{\partial h}{\partial y}
    /// \end{align}
    /// ```
    ///
    /// where `$\frac{\partial F}{\partial X}$` for any `$F \in \{ h, u, v \}$`
    /// is computed for grid cell `$(i, j)$` using the centered difference
    /// approximation along the x- or y-axis:
    ///
    /// ```math
    /// \begin{align}
    ///     { \left( \frac{\partial F}{\partial x} \right) }_{(i, j)} &=
    ///         \frac{F_{(i+1, j)} - F_{(i-1, j)}}{2 \Delta x} \newline
    ///     { \left( \frac{\partial F}{\partial y} \right) }_{(i, j)} &=
    ///         \frac{F_{(i, j+1)} - F_{(i, j-1)}}{2 \Delta y}
    /// \end{align}
    /// ```
    ///
    /// The model's state has three variables, `h`, `u`, and `v`, which are of
    /// shape `$(y_{dim}, x_{dim})$`.
    ///
    /// [SIGNATURE]: # "(params: types.TwoDSWParameters, stepping: TimeStepping, boundary: Boundary, dt: float) -> Model"
    #[must_use]
    pub fn twodsw(
        params: Dataclass<core_model::model::twodsw::TwoDSWParameters<f64>>,
        stepping: &TimeStepping,
        boundary: &Boundary,
        dt: f64,
    ) -> Self {
        let (model, ext) = core_model::model::any::AnyModel::new(
            core_model::model::twodsw::TwoDSW::new(*params),
            Box::new(()),
        );
        let stepping = stepping.as_any(&model);
        let boundary = boundary.as_any();

        Self {
            model,
            ext,
            stepping,
            boundary,
            dt,
        }
    }
}

impl Clone for Model {
    fn clone(&self) -> Self {
        Self {
            model: core_model::model::Model::with_state(
                &self.model,
                core_model::model::StateView::to_owned(&core_model::model::Model::state(
                    &self.model,
                )),
            ),
            ext: self.ext.clone(),
            stepping: self.stepping.clone(),
            boundary: self.boundary.clone(),
            dt: self.dt,
        }
    }
}

#[pyclass(module = "fcbench.model", frozen, eq)]
/// The `TimeStepping` enum specifies the time stepping scheme that
/// is used to advance the model by one timestep.
///
/// The following options are supported:
///
/// - [`TimeStepping::ForwardEuler`]: The model is advanced using the (direct)
///   Forward Euler method, which uses the first derivative of a field `$F$`:
///
///     ```math
///     \begin{align}
///         F_{(t + \Delta t)} &= F_{t} + \Delta t \cdot {\left(
///             \frac{\partial F}{\partial t}
///         \right)}_{F_{t}}
///     \end{align}
///     ```
///
///     Note that this method's truncation error is proportional to
///     `$(\Delta t)^2$` and the second time-derivative of `$F$`.
///
/// - [`TimeStepping::Heun`]: The model is advanced using Heun's method, which
///   extrapolates from the previous timestep using the average of the current
///   first derivative of a field `$F$` and a prediction of this derivative
///   after the next timestep.
///
///     ```math
///     \begin{align}
///         F_{(t + \Delta t)}^{*} &= F_{t} + \Delta t \cdot {\left(
///             \frac{\partial F}{\partial t}
///         \right)}_{F_{t}} \newline
///         F_{(t + \Delta t)} &= F_{t} + \frac{\Delta t}{2} \left( {\left(
///             \frac{\partial F}{\partial t}
///         \right)}_{F_{t}} + {\left(
///             \frac{\partial F}{\partial t}
///         \right)}_{F_{(t + \Delta t)}^{*}} \right) \newline
///     \end{align}
///     ```
///
///     Equivalently, the method can be seen to averages between the current
///     state of a field `$F$` and a double-[`TimeStepping::ForwardEuler`]
///     estimate for the state after two timesteps:
///
///     ```math
///     \begin{align}
///         F_{(t + \Delta t)}^{*} &= F_{t} + \Delta t \cdot {\left(
///             \frac{\partial F}{\partial t}
///         \right)}_{F_{t}} \newline
///         F_{(t + 2 \Delta t)}^{*} &= F_{(t + \Delta t)}^{*} + \Delta t \cdot
///         {\left(
///             \frac{\partial F}{\partial t}
///         \right)}_{F_{(t + \Delta t)}^{*}} \newline
///         F_{(t + \Delta t)} &= \left(
///             F_{t} + F_{(t + 2 \Delta t)}^{*}
///         \right) \cdot 0.5
///     \end{align}
///     ```
///
///     Note that this method's truncation error is proportional to
///     `$(\Delta t)^3$`.
///
/// - [`TimeStepping::LeapFrog`]: The model is advanced using the Leap Frog
///   method, which extrapolates from the previous timestep using the first
///   derivative of a field `$F$` in the current timestep:
///
///     ```math
///     \begin{align}
///         F_{(t + \Delta t)} &= F_{(t - \Delta t)} + 2 \Delta t \cdot {\left(
///             \frac{\partial F}{\partial t}
///         \right)}_{F_{t}}
///     \end{align}
///     ```
///
///     Note that this method's truncation error is proportional to
///     `$(\Delta t)^3$` and the third time-derivative of `$F$`.
///
/// - [`TimeStepping::RungeKutta4`]: The model is advanced using the 4th order
///   Runge-Kutta method, which averages the estimates of the first derivative
///   tendencies of a field `$F$` at `$t$`, `$t + 0.5 \cdot \Delta t$`, and `$t
///   + \Delta t$`:
///
///     ```math
///     \begin{align}
///         F_{(t + \Delta t)} &= F_{t} + \frac{\Delta t}{6} \left(
///             k_1 + 2 k_2 + 2 k_3 + k_4
///         \right)
///     \end{align}
///     ```
///
///     where
///
///     ```math
///     \begin{align}
///         k_1 &= {\left(
///             \frac{\partial F}{\partial t}
///         \right)}_{F_{t}} \newline
///         k_2 &= {\left(
///             \frac{\partial F}{\partial t}
///         \right)}_{F_{t} + 0.5 \cdot \Delta t \cdot k_1} \newline
///         k_3 &= {\left(
///             \frac{\partial F}{\partial t}
///         \right)}_{F_{t} + 0.5 \cdot \Delta t \cdot k_2} \newline
///         k_4 &= {\left(
///             \frac{\partial F}{\partial t}
///         \right)}_{F_{t} + \Delta t \cdot k_3}
///     \end{align}
///     ```
///
///     Note that this method's truncation error is proportional to
///     `$(\Delta t)^5$` and the fourth time-derivative of `$F$`.
#[derive(PartialEq, Eq)]
pub enum TimeStepping {
    /// The model is advanced using the (direct) Forward Euler method, which
    /// uses the first derivative.
    ForwardEuler,
    /// The model is advanced using Heun's method, which extrapolates from
    /// the previous timestep using the average of the current first derivative
    /// and a prediction of this derivative after the next timestep.
    Heun,
    /// The model is advanced using the Leap Frog method, which extrapolates
    /// from the previous timestep using the first derivative in the current
    /// timestep.
    LeapFrog,
    /// The model is advanced using the 4th order Runge-Kutta method, which
    /// averages the estimates of the first derivative tendencies of a field
    /// `$F$` at `$t$`, `$t + 0.5 \cdot \Delta t$`, and `$t + \Delta t$`.
    RungeKutta4,
}

impl TimeStepping {
    fn as_any(
        &self,
        model: &core_model::model::any::AnyModel<f64>,
    ) -> core_model::stepping::AnyTimeStepping<f64> {
        match self {
            Self::ForwardEuler => core_model::stepping::AnyTimeStepping::new(
                core_model::stepping::ForwardEuler::new(model),
            ),
            Self::Heun => {
                core_model::stepping::AnyTimeStepping::new(core_model::stepping::Heun::new(model))
            },
            Self::LeapFrog => {
                core_model::stepping::AnyTimeStepping::new(core_model::stepping::LeapFrog::new(
                    model,
                    core_model::model::StateView::to_owned(&core_model::model::Model::state(model)),
                ))
            },
            Self::RungeKutta4 => core_model::stepping::AnyTimeStepping::new(
                core_model::stepping::RungeKutta4::new(model),
            ),
        }
    }
}

#[pyclass(module = "fcbench.model", frozen, eq)]
/// The `Boundary` enum specifies the boundary condition of the model domain.
///
/// The following options are supported:
///
/// - [`Boundary::Periodic`]: The boundary values copy the opposite-boundary
///   adjacent values to produce a periodic domain.
///
///     Specifically, `F[0] = F[dim-2]` and `F[dim-1] = F[1]` for a gridded
///     field `$F$` that is indexed by `$i \in \{ 0, ..., dim - 1 \}$` along
///     each of its axes.
///
/// - [`Boundary::Reflective`]: The boundary values are copy-extended to produce
///   a reflective domain.
///
///     Specifically, `F[0] = F[1]` and `F[dim-1] = F[dim-2]` for a gridded
///     field `$F$` that is indexed by `$i \in \{ 0, ..., dim - 1 \}$` along
///     each of its axes.
///
/// - [`Boundary::Zero`]: The boundary values are constant zero.
///
///     Specifically, `F[0] = F[dim-1] = 0` for a gridded field `$F$` that is
///     indexed by `$i \in \{ 0, ..., dim - 1 \}$` along each of its axes.
#[derive(PartialEq, Eq)]
pub enum Boundary {
    /// The boundary values copy the opposite-boundary adjacent values to
    /// produce a periodic domain.
    Periodic,
    /// The boundary values are copy-extended to produce a reflective domain.
    Reflective,
    /// The boundary values are constant zero.
    Zero,
}

impl Boundary {
    fn as_any(&self) -> core_model::boundary::AnyBoundary<f64> {
        match self {
            Self::Periodic => {
                core_model::boundary::AnyBoundary::new(core_model::boundary::PeriodicBoundary::<1>)
            },
            Self::Reflective => core_model::boundary::AnyBoundary::new(
                core_model::boundary::ReflectiveBoundary::<1>,
            ),
            Self::Zero => {
                core_model::boundary::AnyBoundary::new(core_model::boundary::ZeroBoundary::<1>)
            },
        }
    }
}

#[derive(Clone, serde::Serialize, serde::Deserialize)]
enum Lorenz96Forcing {
    Const(core_model::model::lorenz_96::Const<f64>),
    Distr(core_model::model::lorenz_96::Distr<f64, rand_distr::Normal<f64>>),
}

impl core_model::model::lorenz_96::ForcingSampler for Lorenz96Forcing {
    type Dtype = f64;
    type Ext = ();

    fn sample(&self, _ext: &mut Self::Ext) -> Self::Dtype {
        42.0
    }
}

#[cfg(test)]
mod tests {
    #[test]
    fn dataclass_registry() {
        let _ = super::dataclass_registry();
    }
}
