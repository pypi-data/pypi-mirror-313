use std::{
    borrow::Cow,
    collections::{hash_map::Entry, HashMap},
    convert::Infallible,
    marker::PhantomData,
    ops::Deref,
};

use convert_case::{Case, Casing};
use nonempty::NonEmpty;
use pyo3::{
    exceptions::PyValueError,
    intern,
    prelude::*,
    sync::GILOnceCell,
    types::{
        IntoPyDict, PyBool, PyBytes, PyDict, PyFloat, PyInt, PyList, PyMapping, PyMappingProxy,
        PyString, PyTuple, PyType,
    },
    PyTypeInfo,
};
use pythonize::{PythonizeMappingType, PythonizeNamedMappingType, PythonizeTypes};

mod de;
mod ser;

pub struct Dataclass<T: serde::Serialize> {
    data: T,
}

impl<T: serde::Serialize> Dataclass<T> {
    #[must_use]
    pub const fn new(data: T) -> Self {
        Self { data }
    }

    #[must_use]
    pub fn into_data(self) -> T {
        self.data
    }

    pub fn output(&self, py: Python) -> Result<DataclassOut<T>, PyErr> {
        DataclassOut::new(&self.data, py)
    }

    pub fn output_frozen(&self, py: Python) -> Result<DataclassOutFrozen<T>, PyErr> {
        DataclassOutFrozen::new(&self.data, py)
    }
}

impl<T: serde::Serialize> Deref for Dataclass<T> {
    type Target = T;

    fn deref(&self) -> &Self::Target {
        &self.data
    }
}

impl<'py, T: serde::Serialize + serde::Deserialize<'py>> FromPyObject<'py> for Dataclass<T> {
    fn extract_bound(obj: &Bound<'py, PyAny>) -> Result<Self, PyErr> {
        let mut depythonizer = pythonize::Depythonizer::from_object(obj);

        match serde_path_to_error::deserialize(&mut depythonizer) {
            Ok(data) => Ok(Self { data }),
            Err(err) => {
                let err_with_path =
                    PyValueError::new_err(format!("failed to extract at {}", err.path()));
                err_with_path.set_cause(obj.py(), Some(PyErr::from(err.into_inner())));
                Err(err_with_path)
            },
        }
    }
}

pub struct DataclassOut<T: serde::Serialize> {
    data: Py<PyAny>,
    inner: PhantomData<fn(T)>,
}

impl<T: serde::Serialize> DataclassOut<T> {
    pub fn new(data: &T, py: Python) -> Result<Self, PyErr> {
        match pythonize::pythonize_custom::<PythonizeDataclass, T>(py, data) {
            Ok(data) => Ok(Self {
                data: data.unbind(),
                inner: PhantomData::<fn(T)>,
            }),
            Err(err) => Err(PyErr::from(err)),
        }
    }
}

impl<'py, T: serde::Serialize> IntoPyObject<'py> for DataclassOut<T> {
    type Error = Infallible;
    type Output = Bound<'py, Self::Target>;
    type Target = PyAny;

    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        Ok(self.data.into_bound(py))
    }
}

pub struct DataclassOutFrozen<T: serde::Serialize> {
    data: Py<PyAny>,
    inner: PhantomData<T>,
}

impl<T: serde::Serialize> DataclassOutFrozen<T> {
    pub fn new(data: &T, py: Python) -> Result<Self, PyErr> {
        match pythonize::pythonize_custom::<PythonizeFrozenDataclass, T>(py, data) {
            Ok(data) => Ok(Self {
                data: data.unbind(),
                inner: PhantomData::<T>,
            }),
            Err(err) => Err(PyErr::from(err)),
        }
    }
}

pub struct DataclassRegistry {
    tracer: serde_reflection::Tracer,
    samples: serde_reflection::Samples,
    names: HashMap<&'static str, &'static str>,
}

impl DataclassRegistry {
    #[must_use]
    pub fn new() -> Self {
        Self {
            tracer: serde_reflection::Tracer::new(
                serde_reflection::TracerConfig::default()
                    // prefer binary inputs over human-readable string inputs,
                    //  which often require more validation
                    .is_human_readable(false)
                    // record all types of containers
                    .record_samples_for_newtype_structs(true)
                    .record_samples_for_structs(true)
                    .record_samples_for_tuple_structs(true)
                    // allow tracing NonZero* integer types
                    .default_u8_value(1)
                    .default_u16_value(1)
                    .default_u32_value(1)
                    .default_u64_value(1)
                    .default_u128_value(1)
                    .default_i8_value(1)
                    .default_i16_value(1)
                    .default_i32_value(1)
                    .default_i64_value(1)
                    .default_i128_value(1),
            ),
            samples: serde_reflection::Samples::new(),
            names: HashMap::new(),
        }
    }

    pub fn insert<'a, T: serde::Serialize + serde::Deserialize<'a>>(&'a mut self) {
        #[expect(clippy::expect_used)]
        let (_format, _guesses) = de::DeserializeSeed::<T>::with(&mut self.names, |seed| {
            self.tracer.trace_type_with_seed(&self.samples, seed)
        })
        .expect("DataclassRegistry::insert failed");
    }

    pub fn insert_with_sample<'a, T: serde::Serialize + serde::Deserialize<'a>>(
        &'a mut self,
        sample: &T,
    ) {
        #[expect(clippy::expect_used)]
        ser::Serialize::with(sample, &mut self.names, |sample| {
            self.tracer.trace_value(&mut self.samples, sample)
        })
        .expect("DataclassRegistry::insert_with_sample failed on sample");
    }

    #[expect(clippy::too_many_lines)]
    pub fn export<'py>(
        self,
        py: Python<'py>,
        module: Borrowed<'_, 'py, PyModule>,
    ) -> Result<(), PyErr> {
        #[expect(clippy::expect_used)]
        let mut registry = self
            .tracer
            .registry()
            .expect("DataclassRegistry::export failed with incomplete types");

        let mut unique_to_name = self
            .names
            .into_iter()
            .map(|(unique, name)| (unique, Cow::Borrowed(name)))
            .collect::<HashMap<_, _>>();
        let mut name_to_unique = HashMap::with_capacity(unique_to_name.len());
        for (&unique, name) in &unique_to_name {
            match name_to_unique.entry(name.clone()) {
                Entry::Vacant(entry) => {
                    entry.insert(NonEmpty::new(unique));
                },
                Entry::Occupied(mut entry) => entry.get_mut().push(unique),
            }
        }

        let mut extra_containers = Vec::new();
        for (name, format) in &mut registry {
            if let serde_reflection::ContainerFormat::Enum(variants) = format {
                let enum_name = Self::normalise_type_name(name, &unique_to_name, &name_to_unique);
                for format in variants.values_mut() {
                    let variant_type_name = format!(
                        "{}_{}",
                        enum_name.name,
                        format.name.to_case(Case::UpperCamel)
                    );
                    match &format.value {
                        #[expect(clippy::unreachable)]
                        serde_reflection::VariantFormat::Variable(_) => {
                            unreachable!("{name}::{} is an unresolved variant type", format.name)
                        },
                        serde_reflection::VariantFormat::Unit => (),
                        serde_reflection::VariantFormat::NewType(newtype) => {
                            if let serde_reflection::Format::TypeName(inner_name) = &**newtype {
                                if Self::normalise_type_name(
                                    inner_name,
                                    &unique_to_name,
                                    &name_to_unique,
                                )
                                .name
                                    == format.name
                                {
                                    continue;
                                }
                            }

                            extra_containers.push((
                                variant_type_name.clone(),
                                serde_reflection::ContainerFormat::Struct(vec![
                                    serde_reflection::Named {
                                        name: format.name.clone(),
                                        value: (**newtype).clone(),
                                    },
                                ]),
                            ));
                            format.value = serde_reflection::VariantFormat::NewType(Box::new(
                                serde_reflection::Format::TypeName(variant_type_name),
                            ));
                        },
                        #[expect(clippy::unreachable)]
                        serde_reflection::VariantFormat::Tuple(_) => {
                            unreachable!("{name}::{} is an unsupported tuple variant", format.name)
                        },
                        serde_reflection::VariantFormat::Struct(fields) => {
                            extra_containers.push((
                                variant_type_name.clone(),
                                serde_reflection::ContainerFormat::Struct(fields.clone()),
                            ));
                            format.value = serde_reflection::VariantFormat::NewType(Box::new(
                                serde_reflection::Format::TypeName(variant_type_name),
                            ));
                        },
                    }
                }
            }
        }
        registry.extend(extra_containers);

        let mut newly_unique_names = Vec::new();
        for (name, clashes) in &name_to_unique {
            let type_name =
                Self::normalise_type_name(clashes.head, &unique_to_name, &name_to_unique);
            if !type_name.generics.is_empty() || clashes.tail.is_empty() {
                continue;
            }

            for &unique in clashes {
                #[expect(clippy::panic)]
                let Some(ty) = registry.remove(unique) else {
                    panic!("registry is missing non-generic non-unique type {unique}");
                };

                #[expect(clippy::panic)]
                let serde_reflection::ContainerFormat::Enum(variants) = &ty
                else {
                    panic!("only non-generic non-unique enums are supported");
                };

                assert!(
                    variants.len() == 1,
                    "only single-variant non-generic non-unique enums are supported"
                );
                #[expect(clippy::panic)]
                let Some((_, variant)) = variants.first_key_value() else {
                    panic!("only single-variant non-generic non-unique enums are supported");
                };

                let variant_type_name =
                    format!("{}_{}", name, variant.name.to_case(Case::UpperCamel));
                newly_unique_names.push((unique, variant_type_name));
                registry.insert(String::from(unique), ty);
            }
        }
        for (unique, name) in newly_unique_names {
            unique_to_name.insert(unique, Cow::Owned(name.clone()));
            name_to_unique.insert(Cow::Owned(name), NonEmpty::new(unique));
        }

        for (name, format) in &registry {
            if let serde_reflection::ContainerFormat::Struct(_)
            | serde_reflection::ContainerFormat::Enum(_) = format
            {
                let generics =
                    Self::normalise_type_name(name, &unique_to_name, &name_to_unique).generics;
                for i in 0..generics.len() {
                    let param = if i == 0 {
                        String::from("T")
                    } else {
                        format!("T{}", i + 1)
                    };
                    if !module.hasattr(param.as_str())? {
                        module.add(param.as_str(), type_var(py)?.call1((param.as_str(),))?)?;
                    }
                }
            }
        }

        for (name, format) in &registry {
            if let serde_reflection::ContainerFormat::Struct(_)
            | serde_reflection::ContainerFormat::Enum(_) = format
            {
                let generic_name =
                    Self::normalise_type_name(name, &unique_to_name, &name_to_unique).name;
                if !module.hasattr(&*generic_name)? {
                    let ty = Self::container_type_hint(
                        py,
                        name,
                        format,
                        &registry,
                        &unique_to_name,
                        &name_to_unique,
                        &[],
                    )?;
                    module.add(&*generic_name, ty)?;
                }
            }
        }

        Ok(())
    }

    fn normalise_type_name<'a>(
        unique: &'a str,
        unique_to_name: &HashMap<&'static str, Cow<'static, str>>,
        name_to_unique: &HashMap<Cow<'static, str>, NonEmpty<&'static str>>,
    ) -> TypeName<'a> {
        let Some(name) = unique_to_name.get(unique).cloned() else {
            return TypeName {
                name: Cow::Borrowed(unique),
                generics: Vec::new(),
            };
        };

        #[expect(clippy::expect_used)]
        let clashes = name_to_unique
            .get(&name)
            .expect("container type name should not be dangling");

        if clashes.tail.is_empty() && clashes.head == unique {
            return TypeName {
                name,
                generics: Vec::new(),
            };
        }

        let generics = unique
            .split(&['<', '>', ','])
            .skip(1)
            .filter_map(|generic| {
                if generic.trim().is_empty() {
                    return None;
                }

                #[expect(clippy::expect_used)]
                let generic = unique_to_name
                    .get(generic.trim())
                    .cloned()
                    .expect("generic should resolve to a name");
                Some(generic)
            })
            .collect::<Vec<_>>();

        TypeName { name, generics }
    }

    #[expect(clippy::too_many_lines)]
    fn container_type_hint<'py>(
        py: Python<'py>,
        name: &str,
        format: &serde_reflection::ContainerFormat,
        registry: &serde_reflection::Registry,
        unique_to_name: &HashMap<&'static str, Cow<'static, str>>,
        name_to_unique: &HashMap<Cow<'static, str>, NonEmpty<&'static str>>,
        generics: &[Cow<'static, str>],
    ) -> Result<Bound<'py, PyAny>, PyErr> {
        static MAKE_DATACLASS: GILOnceCell<Py<PyAny>> = GILOnceCell::new();

        match format {
            serde_reflection::ContainerFormat::UnitStruct => Ok(py.None().into_bound(py)),
            serde_reflection::ContainerFormat::NewTypeStruct(inner) => Self::format_type_hint(
                py,
                name,
                Field::Tuple(0),
                inner,
                registry,
                unique_to_name,
                name_to_unique,
                generics,
            ),
            serde_reflection::ContainerFormat::TupleStruct(fields) => Ok(PyTuple::type_object(py)
                .get_item(PyTuple::new(
                    py,
                    fields
                        .iter()
                        .enumerate()
                        .map(|(i, field)| {
                            Self::format_type_hint(
                                py,
                                name,
                                Field::Tuple(i),
                                field,
                                registry,
                                unique_to_name,
                                name_to_unique,
                                generics,
                            )
                        })
                        .collect::<Result<Vec<_>, _>>()?,
                )?)?),
            serde_reflection::ContainerFormat::Struct(fields) => {
                let type_name = Self::normalise_type_name(name, unique_to_name, name_to_unique);
                let generics = type_name
                    .generics
                    .iter()
                    .enumerate()
                    .map(|(i, _generic)| -> Result<_, PyErr> {
                        type_var(py)?.call1((if i == 0 {
                            String::from("T")
                        } else {
                            format!("T{}", i + 1)
                        },))
                    })
                    .collect::<Result<Vec<_>, _>>()?;
                let mut bases = vec![mapping(py)?.clone()];
                if !generics.is_empty() {
                    bases.push(generic(py)?.get_item(PyTuple::new(py, generics)?)?);
                }
                Ok(MAKE_DATACLASS
                    .import(py, "dataclasses", "make_dataclass")?
                    .call(
                        (
                            type_name.name,
                            PyTuple::new(
                                py,
                                fields
                                    .iter()
                                    .map(|field| -> Result<_, PyErr> {
                                        Ok((
                                            field.name.as_str(),
                                            Self::format_type_hint(
                                                py,
                                                name,
                                                Field::Struct(&field.name),
                                                &field.value,
                                                registry,
                                                unique_to_name,
                                                name_to_unique,
                                                &type_name.generics,
                                            )?,
                                        ))
                                    })
                                    .collect::<Result<Vec<_>, _>>()?,
                            )?,
                        ),
                        Some(
                            &[
                                (intern!(py, "bases"), PyTuple::new(py, bases)?.as_any()),
                                (intern!(py, "kw_only"), PyBool::new(py, true).as_any()),
                            ]
                            .into_py_dict(py)?,
                        ),
                    )?)
            },
            serde_reflection::ContainerFormat::Enum(variants) => {
                let type_name = Self::normalise_type_name(name, unique_to_name, name_to_unique);
                let generics = type_name
                    .generics
                    .iter()
                    .enumerate()
                    .map(|(i, _generic)| -> Result<_, PyErr> {
                        type_var(py)?.call1((if i == 0 {
                            String::from("T")
                        } else {
                            format!("T{}", i + 1)
                        },))
                    })
                    .collect::<Result<Vec<_>, _>>()?;
                let mut bases = Vec::with_capacity(1);
                if !generics.is_empty() {
                    bases.push(generic(py)?.get_item(PyTuple::new(py, generics)?)?);
                }
                let bases = PyTuple::new(py, bases)?;
                let namespace = variants
                    .values()
                    .map(|variant| -> Result<_, PyErr> {
                        Ok((
                            variant.name.to_case(Case::UpperCamel),
                            Self::variant_type_hint(
                                py,
                                name,
                                variant,
                                registry,
                                unique_to_name,
                                name_to_unique,
                                &type_name.generics,
                            )?,
                        ))
                    })
                    .collect::<Result<Vec<_>, _>>()?
                    .into_py_dict(py)?;

                PyType::type_object(py).call1((type_name.name, bases, namespace))
            },
        }
    }

    fn variant_type_hint<'py>(
        py: Python<'py>,
        name: &str,
        variant: &serde_reflection::Named<serde_reflection::VariantFormat>,
        registry: &serde_reflection::Registry,
        unique_to_name: &HashMap<&'static str, Cow<'static, str>>,
        name_to_unique: &HashMap<Cow<'static, str>, NonEmpty<&'static str>>,
        generics: &[Cow<'static, str>],
    ) -> Result<Bound<'py, PyAny>, PyErr> {
        match &variant.value {
            #[expect(clippy::unreachable)]
            serde_reflection::VariantFormat::Variable(_) => {
                unreachable!("{name}::{} is an unresolved variant type", variant.name)
            },
            serde_reflection::VariantFormat::Unit => Ok(literal(py)?.get_item(&variant.name)?),
            // FIXME: test matching format in the unit tests
            serde_reflection::VariantFormat::NewType(newtype) => {
                if let serde_reflection::Format::TypeName(newtype) = &**newtype {
                    Self::type_name_hint(
                        py,
                        newtype,
                        registry,
                        unique_to_name,
                        name_to_unique,
                        generics,
                    )
                } else {
                    #[expect(clippy::unreachable)]
                    {
                        unreachable!(
                            "{name}::{} is an unsupported newtype variant - should be handled \
                             earlier",
                            variant.name,
                        )
                    }
                }
            },
            #[expect(clippy::unreachable)]
            serde_reflection::VariantFormat::Tuple(_) => {
                unreachable!("{name}::{} is an unsupported tuple variant", variant.name)
            },
            #[expect(clippy::unreachable)]
            serde_reflection::VariantFormat::Struct(_) => {
                unreachable!(
                    "{name}::{} is an unsupported struct variant - should be handled earlier",
                    variant.name
                )
            },
        }
    }

    #[expect(clippy::too_many_lines, clippy::too_many_arguments)] // FIXME
    fn format_type_hint<'py>(
        py: Python<'py>,
        name: &str,
        field: Field,
        format: &serde_reflection::Format,
        registry: &serde_reflection::Registry,
        unique_to_name: &HashMap<&'static str, Cow<'static, str>>,
        name_to_unique: &HashMap<Cow<'static, str>, NonEmpty<&'static str>>,
        generics: &[Cow<'static, str>],
    ) -> Result<Bound<'py, PyAny>, PyErr> {
        match format {
            #[expect(clippy::unreachable)]
            serde_reflection::Format::Variable(_) => {
                unreachable!("{name}.{field} is an unresolved field type")
            },
            serde_reflection::Format::TypeName(ty) => {
                Self::type_name_hint(py, ty, registry, unique_to_name, name_to_unique, generics)
            },
            serde_reflection::Format::Unit => Ok(py.None().into_bound(py)),
            serde_reflection::Format::Bool => Ok(PyBool::type_object(py).into_any()),
            serde_reflection::Format::I8
            | serde_reflection::Format::I16
            | serde_reflection::Format::I32
            | serde_reflection::Format::I64
            | serde_reflection::Format::I128
            | serde_reflection::Format::U8
            | serde_reflection::Format::U16
            | serde_reflection::Format::U32
            | serde_reflection::Format::U64
            | serde_reflection::Format::U128 => Ok(PyInt::type_object(py).into_any()),
            serde_reflection::Format::F32 | serde_reflection::Format::F64 => {
                Ok(PyFloat::type_object(py).into_any())
            },
            serde_reflection::Format::Char | serde_reflection::Format::Str => {
                Ok(PyString::type_object(py).into_any())
            },
            serde_reflection::Format::Bytes => Ok(PyBytes::type_object(py).into_any()),
            serde_reflection::Format::Option(inner) => {
                Ok(optional(py)?.get_item(Self::format_type_hint(
                    py,
                    name,
                    field,
                    inner,
                    registry,
                    unique_to_name,
                    name_to_unique,
                    generics,
                )?)?)
            },
            serde_reflection::Format::Seq(elem) => {
                Ok(sequence(py)?.get_item(Self::format_type_hint(
                    py,
                    name,
                    field,
                    elem,
                    registry,
                    unique_to_name,
                    name_to_unique,
                    generics,
                )?)?)
            },
            serde_reflection::Format::Map { key, value } => Ok(mapping(py)?.get_item((
                Self::format_type_hint(
                    py,
                    name,
                    field,
                    key,
                    registry,
                    unique_to_name,
                    name_to_unique,
                    generics,
                )?,
                Self::format_type_hint(
                    py,
                    name,
                    field,
                    value,
                    registry,
                    unique_to_name,
                    name_to_unique,
                    generics,
                )?,
            ))?),
            serde_reflection::Format::Tuple(elems) => Ok(PyTuple::type_object(py).get_item(
                elems
                    .iter()
                    .map(|elem| {
                        Self::format_type_hint(
                            py,
                            name,
                            field,
                            elem,
                            registry,
                            unique_to_name,
                            name_to_unique,
                            generics,
                        )
                    })
                    .collect::<Result<Vec<_>, _>>()?,
            )?),
            serde_reflection::Format::TupleArray { content, size } => {
                let elem = Self::format_type_hint(
                    py,
                    name,
                    field,
                    content,
                    registry,
                    unique_to_name,
                    name_to_unique,
                    generics,
                )?;
                Ok(PyTuple::type_object(py)
                    .get_item(PyTuple::new(py, (0..*size).map(|_| &elem))?)?)
            },
        }
    }

    fn type_name_hint<'py>(
        py: Python<'py>,
        name: &str,
        registry: &serde_reflection::Registry,
        unique_to_name: &HashMap<&'static str, Cow<'static, str>>,
        name_to_unique: &HashMap<Cow<'static, str>, NonEmpty<&'static str>>,
        generics: &[Cow<'static, str>],
    ) -> Result<Bound<'py, PyAny>, PyErr> {
        match registry.get(name) {
            Some(
                serde_reflection::ContainerFormat::Struct(_)
                | serde_reflection::ContainerFormat::Enum(_),
            ) => {
                let type_name = Self::normalise_type_name(name, unique_to_name, name_to_unique);
                let mut generic_type_name = String::from(type_name.name);
                if let Some(j) = generics.iter().position(|g| g == &generic_type_name) {
                    assert!(
                        type_name.generics.is_empty(),
                        "unsupported deeply generic struct or enum type"
                    );
                    generic_type_name.clear();
                    generic_type_name.push('T');
                    if j > 0 {
                        generic_type_name.push_str(&format!("{}", j + 1));
                    }
                } else if !type_name.generics.is_empty() {
                    generic_type_name.push('[');
                    for (i, generic) in type_name.generics.into_iter().enumerate() {
                        if i > 0 {
                            generic_type_name.push_str(", ");
                        }
                        if let Some(j) = generics.iter().position(|g| g == &generic) {
                            generic_type_name.push('T');
                            if j > 0 {
                                generic_type_name.push_str(&format!("{}", j + 1));
                            }
                        } else {
                            generic_type_name.push_str(&generic);
                        }
                    }
                    generic_type_name.push(']');
                }
                forwardref(py)?.call1((generic_type_name,))
            },
            Some(format) => Self::container_type_hint(
                py,
                name,
                format,
                registry,
                unique_to_name,
                name_to_unique,
                generics,
            ),
            #[expect(clippy::panic)]
            None => panic!("{name} is an unresolved type"),
        }
    }
}

struct TypeName<'a> {
    name: Cow<'a, str>,
    generics: Vec<Cow<'static, str>>,
}

#[derive(Clone, Copy)]
enum Field<'a> {
    Tuple(usize),
    Struct(&'a str),
}

impl std::fmt::Display for Field<'_> {
    fn fmt(&self, fmt: &mut std::fmt::Formatter) -> std::fmt::Result {
        match self {
            Field::Tuple(idx) => fmt.write_fmt(format_args!("{idx}")),
            Field::Struct(name) => fmt.write_str(name),
        }
    }
}

impl<'py, T: serde::Serialize> IntoPyObject<'py> for DataclassOutFrozen<T> {
    type Error = Infallible;
    type Output = Bound<'py, Self::Target>;
    type Target = PyAny;

    fn into_pyobject(self, py: Python<'py>) -> Result<Self::Output, Self::Error> {
        Ok(self.data.into_bound(py))
    }
}

pub enum PythonizeDataclass {}

impl<'py> PythonizeTypes<'py> for PythonizeDataclass {
    type List = PyList;
    type Map = PyDict;
    type NamedMap = PyNamespaceMappingBuilder<'py>;
}

pub struct PyNamespaceMappingBuilder<'py> {
    name: &'static str,
    dict: Bound<'py, PyDict>,
}

impl<'py> PythonizeNamedMappingType<'py> for PyNamespaceMappingBuilder<'py> {
    type Builder = Self;

    fn builder(py: Python<'py>, _len: usize, name: &'static str) -> PyResult<Self::Builder> {
        Ok(Self {
            name,
            dict: PyDict::new(py),
        })
    }

    fn push_field(
        builder: &mut Self::Builder,
        name: Bound<'py, PyString>,
        value: Bound<'py, PyAny>,
    ) -> PyResult<()> {
        builder.dict.set_item(name, value)
    }

    fn finish(builder: Self::Builder) -> PyResult<Bound<'py, PyMapping>> {
        static SIMPLE_NAMESPACE: GILOnceCell<Py<PyAny>> = GILOnceCell::new();

        let py = builder.dict.py();

        let bases = (
            SIMPLE_NAMESPACE.import(py, "types", "SimpleNamespace")?,
            mutable_mapping(py)?,
        );

        let namespace: Bound<PyDict> = py
            .eval(
                c"dict(
            __getitem__ = lambda self, key: self.__dict__.__getitem__(key),
            __setitem__ = lambda self, key, value: self.__dict__.__setitem__(key, value),
            __delitem__ = lambda self, key: self.__dict__.__delitem__(key),
            __iter__ = lambda self: self.__dict__.__iter__(),
            __len__ = lambda self: self.__dict__.__len__(),
        )",
                None,
                None,
            )?
            .extract()?;

        let class = PyType::type_object(py).call1((builder.name, bases, namespace))?;

        class.call((), Some(&builder.dict))?.extract()
    }
}

pub enum PythonizeFrozenDataclass {}

impl<'py> PythonizeTypes<'py> for PythonizeFrozenDataclass {
    type List = PyTuple;
    type Map = PyFrozenMappingBuilder<'py>;
    type NamedMap = PyFrozenNamespaceMappingBuilder<'py>;
}

pub struct PyFrozenMappingBuilder<'py> {
    dict: Bound<'py, PyDict>,
}

impl<'py> PythonizeMappingType<'py> for PyFrozenMappingBuilder<'py> {
    type Builder = Self;

    fn builder(py: Python<'py>, _len: Option<usize>) -> PyResult<Self::Builder> {
        Ok(Self {
            dict: PyDict::new(py),
        })
    }

    fn push_item(
        builder: &mut Self::Builder,
        name: Bound<'py, PyAny>,
        value: Bound<'py, PyAny>,
    ) -> PyResult<()> {
        builder.dict.set_item(name, value)
    }

    fn finish(builder: Self::Builder) -> PyResult<Bound<'py, PyMapping>> {
        let py = builder.dict.py();

        Ok(PyMappingProxy::new(py, builder.dict.as_mapping())
            .as_mapping()
            .clone())
    }
}

pub struct PyFrozenNamespaceMappingBuilder<'py> {
    name: &'static str,
    dict: Bound<'py, PyDict>,
}

impl<'py> PythonizeNamedMappingType<'py> for PyFrozenNamespaceMappingBuilder<'py> {
    type Builder = Self;

    fn builder(py: Python<'py>, _len: usize, name: &'static str) -> PyResult<Self::Builder> {
        Ok(Self {
            name,
            dict: PyDict::new(py),
        })
    }

    fn push_field(
        builder: &mut Self::Builder,
        name: Bound<'py, PyString>,
        value: Bound<'py, PyAny>,
    ) -> PyResult<()> {
        builder.dict.set_item(name, value)
    }

    fn finish(builder: Self::Builder) -> PyResult<Bound<'py, PyMapping>> {
        static NAMEDTUPLE: GILOnceCell<Py<PyAny>> = GILOnceCell::new();

        let py = builder.dict.py();

        let bases = (
            NAMEDTUPLE
                .import(py, "collections", "namedtuple")?
                .call1((builder.name, builder.dict.keys()))?,
            mapping(py)?,
        );

        let namespace: Bound<PyDict> = py
            .eval(
                c"dict(
            __slots__ = (),
            __getitem__ = lambda self, key: self._asdict().__getitem__(key),
            __iter__ = lambda self: self._fields.__iter__(),
            __contains__ = lambda self, key: self._fields.__contains__(key),
            _asdict = lambda self: { f: v for f, v in zip(self._fields, \
                 type(self).__bases__[0].__iter__(self)) },
        )",
                None,
                None,
            )?
            .extract()?;

        let class = PyType::type_object(py).call1((builder.name, bases, namespace))?;

        class.call((), Some(&builder.dict))?.extract()
    }
}

fn type_var(py: Python) -> Result<&Bound<PyAny>, PyErr> {
    static TYPING_TYPEVAR: GILOnceCell<Py<PyAny>> = GILOnceCell::new();
    TYPING_TYPEVAR.import(py, "typing", "TypeVar")
}

fn generic(py: Python) -> Result<&Bound<PyAny>, PyErr> {
    static TYPING_GENERIC: GILOnceCell<Py<PyAny>> = GILOnceCell::new();
    TYPING_GENERIC.import(py, "typing", "Generic")
}

fn literal(py: Python) -> Result<&Bound<PyAny>, PyErr> {
    static TYPING_LITERAL: GILOnceCell<Py<PyAny>> = GILOnceCell::new();
    TYPING_LITERAL.import(py, "typing", "Literal")
}

fn optional(py: Python) -> Result<&Bound<PyAny>, PyErr> {
    static TYPING_OPTIONAL: GILOnceCell<Py<PyAny>> = GILOnceCell::new();
    TYPING_OPTIONAL.import(py, "typing", "Optional")
}

fn forwardref(py: Python) -> Result<&Bound<PyAny>, PyErr> {
    static TYPING_FORWARDREF: GILOnceCell<Py<PyAny>> = GILOnceCell::new();
    TYPING_FORWARDREF.import(py, "typing", "ForwardRef")
}

fn sequence(py: Python) -> Result<&Bound<PyAny>, PyErr> {
    static COLLECTIONS_ABC_SEQUENCE: GILOnceCell<Py<PyAny>> = GILOnceCell::new();
    COLLECTIONS_ABC_SEQUENCE.import(py, "collections.abc", "Sequence")
}

fn mapping(py: Python) -> Result<&Bound<PyAny>, PyErr> {
    static COLLECTIONS_ABC_MAPPING: GILOnceCell<Py<PyAny>> = GILOnceCell::new();
    COLLECTIONS_ABC_MAPPING.import(py, "collections.abc", "Mapping")
}

fn mutable_mapping(py: Python) -> Result<&Bound<PyAny>, PyErr> {
    static COLLECTIONS_ABC_MUTABLE_MAPPING: GILOnceCell<Py<PyAny>> = GILOnceCell::new();
    COLLECTIONS_ABC_MUTABLE_MAPPING.import(py, "collections.abc", "MutableMapping")
}
