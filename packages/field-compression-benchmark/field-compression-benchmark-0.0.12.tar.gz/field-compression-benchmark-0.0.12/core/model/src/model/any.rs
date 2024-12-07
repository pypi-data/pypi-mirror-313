use std::any::{Any, TypeId};

use dyn_clone::DynClone;
use ndarray::{ArrayView, ArrayViewMut, IxDyn, NdFloat};

use crate::model::{Model, State, StateView, StateViewMut};

pub struct AnyModel<F: NdFloat> {
    model: Box<dyn 'static + ErasedModel<Dtype = F> + Send + Sync>,
}

impl<F: NdFloat> AnyModel<F> {
    #[must_use]
    pub fn new<
        L: 'static
            + Model<
                Dtype = F,
                State: 'static + Send + Sync,
                Ext: 'static + Sized + Send + Sync + Clone,
            >
            + Send
            + Sync,
    >(
        model: L,
        ext: Box<L::Ext>,
    ) -> (Self, AnyExt) {
        (
            Self {
                model: Box::new(model),
            },
            AnyExt { ext },
        )
    }
}

impl<F: NdFloat> Model for AnyModel<F> {
    type Dimension = IxDyn;
    type Dtype = F;
    type Ext = AnyExt;
    type State = AnyState<F>;

    fn variables(&self) -> impl Iterator<Item = &'static str> {
        self.model.variables().into_iter()
    }

    fn state(&self) -> AnyStateView<'_, F> {
        self.model.state()
    }

    fn state_mut(&mut self) -> AnyStateViewMut<'_, F> {
        self.model.state_mut()
    }

    fn tendencies_for_state(
        &self,
        state: AnyStateView<F>,
        tendencies: AnyStateViewMut<F>,
        ext: &mut AnyExt,
    ) {
        self.model.tendencies_for_state(state, tendencies, ext);
    }

    fn with_state(&self, state: AnyState<F>) -> Self {
        self.model.with_state(state)
    }
}

trait ErasedModel {
    type Dtype: NdFloat;

    fn variables(&self) -> Vec<&'static str>;

    fn state(&self) -> AnyStateView<'_, Self::Dtype>;
    fn state_mut(&mut self) -> AnyStateViewMut<'_, Self::Dtype>;

    fn tendencies_for_state(
        &self,
        state: AnyStateView<'_, Self::Dtype>,
        tendencies: AnyStateViewMut<'_, Self::Dtype>,
        ext: &mut AnyExt,
    );

    #[must_use]
    fn with_state(&self, state: AnyState<Self::Dtype>) -> AnyModel<Self::Dtype>;
}

impl<
        L: 'static
            + Model<State: 'static + Send + Sync, Ext: 'static + Sized + Send + Sync>
            + Send
            + Sync,
    > ErasedModel for L
{
    type Dtype = L::Dtype;

    fn variables(&self) -> Vec<&'static str> {
        Model::variables(self).collect()
    }

    fn state(&self) -> AnyStateView<'_, Self::Dtype> {
        AnyStateView {
            view: Box::new(Model::state(self)),
        }
    }

    fn state_mut(&mut self) -> AnyStateViewMut<'_, Self::Dtype> {
        AnyStateViewMut {
            view: Box::new(Model::state_mut(self)),
        }
    }

    fn tendencies_for_state(
        &self,
        state: AnyStateView<'_, Self::Dtype>,
        tendencies: AnyStateViewMut<'_, Self::Dtype>,
        ext: &mut AnyExt,
    ) {
        #[expect(clippy::panic)]
        let Some(ext) = (*ext.ext).as_any().downcast_mut::<L::Ext>() else {
            panic!(
                "AnyModel::tendencies_for_state called with wrong ext: expected {} but found {}",
                std::any::type_name::<L::Ext>(),
                ext.ext.type_name()
            );
        };

        assert!(
            ErasedStateView::type_id(&*state.view)
                == non_static_type_id::<<L::State as State>::View<'_>>(),
            "AnyModel::tendencies_for_state called with wrong state: expected {} but found {}",
            std::any::type_name::<<L::State as State>::View<'_>>(),
            ErasedStateView::type_name(&*state.view)
        );

        #[expect(unsafe_code)]
        // Safety: type cast is checked above
        let state = unsafe {
            let raw: *mut dyn ErasedStateView<Dtype = Self::Dtype> = Box::into_raw(state.view);
            *Box::from_raw(raw.cast::<<L::State as State>::View<'_>>())
        };

        assert!(
            ErasedStateViewMut::type_id(&*tendencies.view)
                == non_static_type_id::<<L::State as State>::ViewMut<'_>>(),
            "AnyModel::tendencies_for_state called with wrong tendencies: expected {} but found {}",
            std::any::type_name::<<L::State as State>::ViewMut<'_>>(),
            ErasedStateViewMut::type_name(&*tendencies.view)
        );

        #[expect(unsafe_code)]
        // Safety: type cast is checked above
        let tendencies = unsafe {
            let raw: *mut dyn ErasedStateViewMut<Dtype = Self::Dtype> =
                Box::into_raw(tendencies.view);
            *Box::from_raw(raw.cast::<<L::State as State>::ViewMut<'_>>())
        };

        Model::tendencies_for_state(self, state, tendencies, ext);
    }

    fn with_state(&self, state: AnyState<Self::Dtype>) -> AnyModel<Self::Dtype> {
        assert!(
            ErasedState::type_id(&*state.state) == non_static_type_id::<L::State>(),
            "AnyModel::with_state called with wrong state: expected {} but found {}",
            std::any::type_name::<L::State>(),
            ErasedState::type_name(&*state.state)
        );
        #[expect(unsafe_code)]
        // Safety: type cast is checked above
        let state = unsafe {
            let raw: *mut dyn ErasedState<Dtype = Self::Dtype> = Box::into_raw(state.state);
            *Box::from_raw(raw.cast::<L::State>())
        };

        AnyModel {
            model: Box::new(Model::with_state(self, state)),
        }
    }
}

trait AnyTypeName: Any {
    fn type_name(&self) -> &'static str;

    fn as_any(&mut self) -> &mut dyn Any;
}

impl<T: Any> AnyTypeName for T {
    fn type_name(&self) -> &'static str {
        std::any::type_name::<Self>()
    }

    fn as_any(&mut self) -> &mut dyn Any {
        self
    }
}

// Courtesy of David Tolnay:
// https://github.com/rust-lang/rust/issues/41875#issuecomment-317292888
fn non_static_type_id<T: ?Sized>() -> TypeId {
    trait NonStaticAny {
        fn get_type_id(&self) -> TypeId
        where
            Self: 'static;
    }

    impl<T: ?Sized> NonStaticAny for std::marker::PhantomData<T> {
        fn get_type_id(&self) -> TypeId
        where
            Self: 'static,
        {
            TypeId::of::<T>()
        }
    }

    let phantom_data = std::marker::PhantomData::<T>;
    #[expect(unsafe_code)]
    // Safety: lifetime extension to 'static is only used to reveal the TypeId
    NonStaticAny::get_type_id(unsafe {
        std::mem::transmute::<&dyn NonStaticAny, &(dyn NonStaticAny + 'static)>(&phantom_data)
    })
}

pub struct AnyExt {
    ext: Box<dyn 'static + ErasedExt + Send + Sync>,
}

impl AnyExt {
    pub fn downcast_mut<T: Any>(&mut self) -> Option<&mut T> {
        self.ext.as_any().downcast_mut()
    }
}

impl Clone for AnyExt {
    fn clone(&self) -> Self {
        Self {
            ext: dyn_clone::clone_box(&*self.ext),
        }
    }
}

trait ErasedExt: AnyTypeName + DynClone {}

impl<T: AnyTypeName + DynClone> ErasedExt for T {}

pub struct AnyState<F: NdFloat> {
    state: Box<dyn 'static + ErasedState<Dtype = F> + Send + Sync>,
}

impl<F: NdFloat> Clone for AnyState<F> {
    fn clone(&self) -> Self {
        ErasedState::clone(&*self.state)
    }
}

impl<F: NdFloat> State for AnyState<F> {
    type Dimension = IxDyn;
    type Dtype = F;
    type View<'a> = AnyStateView<'a, F>;
    type ViewMut<'a> = AnyStateViewMut<'a, F>;

    fn view(&self) -> Self::View<'_> {
        self.state.view()
    }

    fn view_mut(&mut self) -> Self::ViewMut<'_> {
        self.state.view_mut()
    }
}

trait ErasedState {
    type Dtype: NdFloat;

    fn type_id(&self) -> TypeId;
    fn type_name(&self) -> &'static str;

    fn clone(&self) -> AnyState<Self::Dtype>;

    fn view(&self) -> AnyStateView<'_, Self::Dtype>;
    fn view_mut(&mut self) -> AnyStateViewMut<'_, Self::Dtype>;
}

impl<S: 'static + State + Send + Sync> ErasedState for S {
    type Dtype = S::Dtype;

    fn type_id(&self) -> TypeId {
        non_static_type_id::<Self>()
    }

    fn type_name(&self) -> &'static str {
        std::any::type_name::<Self>()
    }

    fn clone(&self) -> AnyState<Self::Dtype> {
        AnyState {
            state: Box::new(Clone::clone(self)),
        }
    }

    fn view(&self) -> AnyStateView<'_, Self::Dtype> {
        AnyStateView {
            view: Box::new(State::view(self)),
        }
    }

    fn view_mut(&mut self) -> AnyStateViewMut<'_, Self::Dtype> {
        AnyStateViewMut {
            view: Box::new(State::view_mut(self)),
        }
    }
}

pub struct AnyStateView<'s, F: NdFloat> {
    view: Box<dyn 's + ErasedStateView<'s, Dtype = F>>,
}

impl<'s, F: NdFloat> StateView for AnyStateView<'s, F> {
    type Dimension = IxDyn;
    type Dtype = F;
    type State = AnyState<F>;

    fn view(&self) -> <Self::State as State>::View<'_> {
        self.view.view()
    }

    fn to_owned(&self) -> Self::State {
        self.view.to_owned()
    }

    fn iter<'a>(
        &'a self,
    ) -> impl Iterator<Item = ArrayView<'a, Self::Dtype, Self::Dimension>> + 'a {
        self.view.iter()
    }
}

trait ErasedStateView<'s> {
    type Dtype: NdFloat;

    fn type_id(&self) -> TypeId;
    fn type_name(&self) -> &'static str;

    fn view(&self) -> AnyStateView<'_, Self::Dtype>;
    fn to_owned(&self) -> AnyState<Self::Dtype>;

    fn iter<'a>(&'a self) -> Box<dyn Iterator<Item = ArrayView<'a, Self::Dtype, IxDyn>> + 'a>;
}

impl<'s, S: 's + StateView<State: 'static + Send + Sync>> ErasedStateView<'s> for S {
    type Dtype = S::Dtype;

    fn type_id(&self) -> TypeId {
        non_static_type_id::<Self>()
    }

    fn type_name(&self) -> &'static str {
        std::any::type_name::<Self>()
    }

    fn view(&self) -> AnyStateView<'_, Self::Dtype> {
        AnyStateView {
            view: Box::new(StateView::view(self)),
        }
    }

    fn to_owned(&self) -> AnyState<Self::Dtype> {
        AnyState {
            state: Box::new(StateView::to_owned(self)),
        }
    }

    fn iter<'a>(&'a self) -> Box<dyn Iterator<Item = ArrayView<'a, Self::Dtype, IxDyn>> + 'a> {
        #[expect(clippy::redundant_closure_for_method_calls)]
        Box::new(StateView::iter(self).map(|array| array.into_dyn()))
    }
}

pub struct AnyStateViewMut<'s, F: NdFloat> {
    view: Box<dyn 's + ErasedStateViewMut<'s, Dtype = F>>,
}

impl<'s, F: NdFloat> StateViewMut for AnyStateViewMut<'s, F> {
    type Dimension = IxDyn;
    type Dtype = F;
    type State = AnyState<F>;

    fn view(&self) -> <Self::State as State>::View<'_> {
        self.view.view()
    }

    fn view_mut(&mut self) -> <Self::State as State>::ViewMut<'_> {
        self.view.view_mut()
    }

    fn to_owned(&self) -> Self::State {
        self.view.to_owned()
    }

    fn iter<'a>(
        &'a self,
    ) -> impl Iterator<Item = ArrayView<'a, Self::Dtype, Self::Dimension>> + 'a {
        self.view.iter()
    }

    fn iter_mut<'a>(
        &'a mut self,
    ) -> impl Iterator<Item = ArrayViewMut<'a, Self::Dtype, Self::Dimension>> + 'a {
        self.view.iter_mut()
    }
}

trait ErasedStateViewMut<'s> {
    type Dtype: NdFloat;

    fn type_id(&self) -> TypeId;
    fn type_name(&self) -> &'static str;

    fn view(&self) -> AnyStateView<'_, Self::Dtype>;
    fn view_mut(&mut self) -> AnyStateViewMut<'_, Self::Dtype>;
    fn to_owned(&self) -> AnyState<Self::Dtype>;

    fn iter<'a>(&'a self) -> Box<dyn Iterator<Item = ArrayView<'a, Self::Dtype, IxDyn>> + 'a>;
    fn iter_mut<'a>(
        &'a mut self,
    ) -> Box<dyn Iterator<Item = ArrayViewMut<'a, Self::Dtype, IxDyn>> + 'a>;
}

impl<S: StateViewMut<State: 'static + Send + Sync>> ErasedStateViewMut<'_> for S {
    type Dtype = S::Dtype;

    fn type_id(&self) -> TypeId {
        non_static_type_id::<Self>()
    }

    fn type_name(&self) -> &'static str {
        std::any::type_name::<Self>()
    }

    fn view(&self) -> AnyStateView<'_, Self::Dtype> {
        AnyStateView {
            view: Box::new(StateViewMut::view(self)),
        }
    }

    fn view_mut(&mut self) -> AnyStateViewMut<'_, Self::Dtype> {
        AnyStateViewMut {
            view: Box::new(StateViewMut::view_mut(self)),
        }
    }

    fn to_owned(&self) -> AnyState<Self::Dtype> {
        AnyState {
            state: Box::new(StateViewMut::to_owned(self)),
        }
    }

    fn iter<'a>(&'a self) -> Box<dyn Iterator<Item = ArrayView<'a, Self::Dtype, IxDyn>> + 'a> {
        #[expect(clippy::redundant_closure_for_method_calls)]
        Box::new(StateViewMut::iter(self).map(|array| array.into_dyn()))
    }

    fn iter_mut<'a>(
        &'a mut self,
    ) -> Box<dyn Iterator<Item = ArrayViewMut<'a, Self::Dtype, IxDyn>> + 'a> {
        #[expect(clippy::redundant_closure_for_method_calls)]
        Box::new(StateViewMut::iter_mut(self).map(|array| array.into_dyn()))
    }
}
