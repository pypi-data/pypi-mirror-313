// Adapted from David Tolnay's serde_path_to_error, which is "licensed under
// either of Apache License, Version 2.0 or MIT license at your option".
// https://github.com/dtolnay/path-to-error/blob/306187eee030e31ac0dc358f0b585c0f82b8a8d7/src/de.rs

use std::{any::type_name, cell::RefCell, collections::HashMap, fmt, marker::PhantomData};

pub struct DeserializeSeed<'a, T> {
    names: &'a RefCell<HashMap<&'static str, &'static str>>,
    _marker: PhantomData<T>,
}

impl<T> Clone for DeserializeSeed<'_, T> {
    fn clone(&self) -> Self {
        Self {
            names: self.names,
            _marker: PhantomData::<T>,
        }
    }
}

impl<T> DeserializeSeed<'_, T> {
    #[must_use]
    pub fn with<R>(
        names: &mut HashMap<&'static str, &'static str>,
        inner: impl for<'b> FnOnce(DeserializeSeed<'b, T>) -> R,
    ) -> R {
        let ref_cell_names = RefCell::new(std::mem::take(names));
        let result = inner(DeserializeSeed {
            names: &ref_cell_names,
            _marker: PhantomData::<T>,
        });
        *names = ref_cell_names.into_inner();
        result
    }
}

impl<'de, T: serde::de::Deserialize<'de>> serde::de::DeserializeSeed<'de>
    for DeserializeSeed<'_, T>
{
    type Value = T;

    fn deserialize<D>(self, deserializer: D) -> Result<Self::Value, D::Error>
    where
        D: serde::Deserializer<'de>,
    {
        T::deserialize(Deserializer {
            de: deserializer,
            names: self.names,
        })
    }
}

struct Deserializer<'a, D> {
    de: D,
    names: &'a RefCell<HashMap<&'static str, &'static str>>,
}

struct Wrap<'a, X> {
    delegate: X,
    names: &'a RefCell<HashMap<&'static str, &'static str>>,
}

impl<'de, D> serde::de::Deserializer<'de> for Deserializer<'_, D>
where
    D: serde::de::Deserializer<'de>,
{
    type Error = D::Error;

    fn deserialize_any<V>(self, visitor: V) -> Result<V::Value, D::Error>
    where
        V: serde::de::Visitor<'de>,
    {
        self.de.deserialize_any(Wrap {
            delegate: visitor,
            names: self.names,
        })
    }

    fn deserialize_bool<V>(self, visitor: V) -> Result<V::Value, D::Error>
    where
        V: serde::de::Visitor<'de>,
    {
        self.de.deserialize_bool(Wrap {
            delegate: visitor,
            names: self.names,
        })
    }

    fn deserialize_u8<V>(self, visitor: V) -> Result<V::Value, D::Error>
    where
        V: serde::de::Visitor<'de>,
    {
        self.de.deserialize_u8(Wrap {
            delegate: visitor,
            names: self.names,
        })
    }

    fn deserialize_u16<V>(self, visitor: V) -> Result<V::Value, D::Error>
    where
        V: serde::de::Visitor<'de>,
    {
        self.de.deserialize_u16(Wrap {
            delegate: visitor,
            names: self.names,
        })
    }

    fn deserialize_u32<V>(self, visitor: V) -> Result<V::Value, D::Error>
    where
        V: serde::de::Visitor<'de>,
    {
        self.de.deserialize_u32(Wrap {
            delegate: visitor,
            names: self.names,
        })
    }

    fn deserialize_u64<V>(self, visitor: V) -> Result<V::Value, D::Error>
    where
        V: serde::de::Visitor<'de>,
    {
        self.de.deserialize_u64(Wrap {
            delegate: visitor,
            names: self.names,
        })
    }

    fn deserialize_u128<V>(self, visitor: V) -> Result<V::Value, D::Error>
    where
        V: serde::de::Visitor<'de>,
    {
        self.de.deserialize_u128(Wrap {
            delegate: visitor,
            names: self.names,
        })
    }

    fn deserialize_i8<V>(self, visitor: V) -> Result<V::Value, D::Error>
    where
        V: serde::de::Visitor<'de>,
    {
        self.de.deserialize_i8(Wrap {
            delegate: visitor,
            names: self.names,
        })
    }

    fn deserialize_i16<V>(self, visitor: V) -> Result<V::Value, D::Error>
    where
        V: serde::de::Visitor<'de>,
    {
        self.de.deserialize_i16(Wrap {
            delegate: visitor,
            names: self.names,
        })
    }

    fn deserialize_i32<V>(self, visitor: V) -> Result<V::Value, D::Error>
    where
        V: serde::de::Visitor<'de>,
    {
        self.de.deserialize_i32(Wrap {
            delegate: visitor,
            names: self.names,
        })
    }

    fn deserialize_i64<V>(self, visitor: V) -> Result<V::Value, D::Error>
    where
        V: serde::de::Visitor<'de>,
    {
        self.de.deserialize_i64(Wrap {
            delegate: visitor,
            names: self.names,
        })
    }

    fn deserialize_i128<V>(self, visitor: V) -> Result<V::Value, D::Error>
    where
        V: serde::de::Visitor<'de>,
    {
        self.de.deserialize_i128(Wrap {
            delegate: visitor,
            names: self.names,
        })
    }

    fn deserialize_f32<V>(self, visitor: V) -> Result<V::Value, D::Error>
    where
        V: serde::de::Visitor<'de>,
    {
        self.de.deserialize_f32(Wrap {
            delegate: visitor,
            names: self.names,
        })
    }

    fn deserialize_f64<V>(self, visitor: V) -> Result<V::Value, D::Error>
    where
        V: serde::de::Visitor<'de>,
    {
        self.de.deserialize_f64(Wrap {
            delegate: visitor,
            names: self.names,
        })
    }

    fn deserialize_char<V>(self, visitor: V) -> Result<V::Value, D::Error>
    where
        V: serde::de::Visitor<'de>,
    {
        self.de.deserialize_char(Wrap {
            delegate: visitor,
            names: self.names,
        })
    }

    fn deserialize_str<V>(self, visitor: V) -> Result<V::Value, D::Error>
    where
        V: serde::de::Visitor<'de>,
    {
        self.de.deserialize_str(Wrap {
            delegate: visitor,
            names: self.names,
        })
    }

    fn deserialize_string<V>(self, visitor: V) -> Result<V::Value, D::Error>
    where
        V: serde::de::Visitor<'de>,
    {
        self.de.deserialize_string(Wrap {
            delegate: visitor,
            names: self.names,
        })
    }

    fn deserialize_bytes<V>(self, visitor: V) -> Result<V::Value, D::Error>
    where
        V: serde::de::Visitor<'de>,
    {
        self.de.deserialize_bytes(Wrap {
            delegate: visitor,
            names: self.names,
        })
    }

    fn deserialize_byte_buf<V>(self, visitor: V) -> Result<V::Value, D::Error>
    where
        V: serde::de::Visitor<'de>,
    {
        self.de.deserialize_byte_buf(Wrap {
            delegate: visitor,
            names: self.names,
        })
    }

    fn deserialize_option<V>(self, visitor: V) -> Result<V::Value, D::Error>
    where
        V: serde::de::Visitor<'de>,
    {
        self.de.deserialize_option(Wrap {
            delegate: visitor,
            names: self.names,
        })
    }

    fn deserialize_unit<V>(self, visitor: V) -> Result<V::Value, D::Error>
    where
        V: serde::de::Visitor<'de>,
    {
        self.de.deserialize_unit(Wrap {
            delegate: visitor,
            names: self.names,
        })
    }

    fn deserialize_unit_struct<V>(
        self,
        name: &'static str,
        visitor: V,
    ) -> Result<V::Value, D::Error>
    where
        V: serde::de::Visitor<'de>,
    {
        self.names
            .borrow_mut()
            .insert(type_name::<V::Value>(), name);
        let name = type_name::<V::Value>();

        self.de.deserialize_unit_struct(
            name,
            Wrap {
                delegate: visitor,
                names: self.names,
            },
        )
    }

    fn deserialize_newtype_struct<V>(
        self,
        name: &'static str,
        visitor: V,
    ) -> Result<V::Value, D::Error>
    where
        V: serde::de::Visitor<'de>,
    {
        self.names
            .borrow_mut()
            .insert(type_name::<V::Value>(), name);
        let name = type_name::<V::Value>();

        self.de.deserialize_newtype_struct(
            name,
            Wrap {
                delegate: visitor,
                names: self.names,
            },
        )
    }

    fn deserialize_seq<V>(self, visitor: V) -> Result<V::Value, D::Error>
    where
        V: serde::de::Visitor<'de>,
    {
        // Workaround for non-empty containers
        //  - ideally there would be a canary to use this just for
        //    `nonempty::NonEmpty<T>`, but `NonEmpty` deserialises from a `Vec<T>` using
        //    its `TryFrom` impl
        // FIXME: remove once supported in serde-reflection:
        // https://github.com/zefchain/serde-reflection/pull/41
        self.de.deserialize_tuple(
            1,
            Wrap {
                delegate: visitor,
                names: self.names,
            },
        )
    }

    fn deserialize_tuple<V>(self, len: usize, visitor: V) -> Result<V::Value, D::Error>
    where
        V: serde::de::Visitor<'de>,
    {
        self.de.deserialize_tuple(
            len,
            Wrap {
                delegate: visitor,
                names: self.names,
            },
        )
    }

    fn deserialize_tuple_struct<V>(
        self,
        name: &'static str,
        len: usize,
        visitor: V,
    ) -> Result<V::Value, D::Error>
    where
        V: serde::de::Visitor<'de>,
    {
        self.names
            .borrow_mut()
            .insert(type_name::<V::Value>(), name);
        let name = type_name::<V::Value>();

        self.de.deserialize_tuple_struct(
            name,
            len,
            Wrap {
                delegate: visitor,
                names: self.names,
            },
        )
    }

    fn deserialize_map<V>(self, visitor: V) -> Result<V::Value, D::Error>
    where
        V: serde::de::Visitor<'de>,
    {
        self.de.deserialize_map(Wrap {
            delegate: visitor,
            names: self.names,
        })
    }

    fn deserialize_struct<V>(
        self,
        name: &'static str,
        fields: &'static [&'static str],
        visitor: V,
    ) -> Result<V::Value, D::Error>
    where
        V: serde::de::Visitor<'de>,
    {
        self.names
            .borrow_mut()
            .insert(type_name::<V::Value>(), name);
        let name = type_name::<V::Value>();

        self.de.deserialize_struct(
            name,
            fields,
            Wrap {
                delegate: visitor,
                names: self.names,
            },
        )
    }

    fn deserialize_enum<V>(
        self,
        name: &'static str,
        variants: &'static [&'static str],
        visitor: V,
    ) -> Result<V::Value, D::Error>
    where
        V: serde::de::Visitor<'de>,
    {
        self.names
            .borrow_mut()
            .insert(type_name::<V::Value>(), name);
        let name = type_name::<V::Value>();

        self.de.deserialize_enum(
            name,
            variants,
            Wrap {
                delegate: visitor,
                names: self.names,
            },
        )
    }

    fn deserialize_ignored_any<V>(self, visitor: V) -> Result<V::Value, D::Error>
    where
        V: serde::de::Visitor<'de>,
    {
        self.de.deserialize_ignored_any(Wrap {
            delegate: visitor,
            names: self.names,
        })
    }

    fn deserialize_identifier<V>(self, visitor: V) -> Result<V::Value, D::Error>
    where
        V: serde::de::Visitor<'de>,
    {
        self.de.deserialize_identifier(Wrap {
            delegate: visitor,
            names: self.names,
        })
    }

    fn is_human_readable(&self) -> bool {
        self.de.is_human_readable()
    }
}

impl<'de, X> serde::de::Visitor<'de> for Wrap<'_, X>
where
    X: serde::de::Visitor<'de>,
{
    type Value = X::Value;

    fn expecting(&self, formatter: &mut fmt::Formatter) -> fmt::Result {
        self.delegate.expecting(formatter)
    }

    fn visit_bool<E>(self, v: bool) -> Result<Self::Value, E>
    where
        E: serde::de::Error,
    {
        self.delegate.visit_bool(v)
    }

    fn visit_i8<E>(self, v: i8) -> Result<Self::Value, E>
    where
        E: serde::de::Error,
    {
        self.delegate.visit_i8(v)
    }

    fn visit_i16<E>(self, v: i16) -> Result<Self::Value, E>
    where
        E: serde::de::Error,
    {
        self.delegate.visit_i16(v)
    }

    fn visit_i32<E>(self, v: i32) -> Result<Self::Value, E>
    where
        E: serde::de::Error,
    {
        self.delegate.visit_i32(v)
    }

    fn visit_i64<E>(self, v: i64) -> Result<Self::Value, E>
    where
        E: serde::de::Error,
    {
        self.delegate.visit_i64(v)
    }

    fn visit_i128<E>(self, v: i128) -> Result<Self::Value, E>
    where
        E: serde::de::Error,
    {
        self.delegate.visit_i128(v)
    }

    fn visit_u8<E>(self, v: u8) -> Result<Self::Value, E>
    where
        E: serde::de::Error,
    {
        self.delegate.visit_u8(v)
    }

    fn visit_u16<E>(self, v: u16) -> Result<Self::Value, E>
    where
        E: serde::de::Error,
    {
        self.delegate.visit_u16(v)
    }

    fn visit_u32<E>(self, v: u32) -> Result<Self::Value, E>
    where
        E: serde::de::Error,
    {
        self.delegate.visit_u32(v)
    }

    fn visit_u64<E>(self, v: u64) -> Result<Self::Value, E>
    where
        E: serde::de::Error,
    {
        self.delegate.visit_u64(v)
    }

    fn visit_u128<E>(self, v: u128) -> Result<Self::Value, E>
    where
        E: serde::de::Error,
    {
        self.delegate.visit_u128(v)
    }

    fn visit_f32<E>(self, v: f32) -> Result<Self::Value, E>
    where
        E: serde::de::Error,
    {
        self.delegate.visit_f32(v)
    }

    fn visit_f64<E>(self, v: f64) -> Result<Self::Value, E>
    where
        E: serde::de::Error,
    {
        self.delegate.visit_f64(v)
    }

    fn visit_char<E>(self, v: char) -> Result<Self::Value, E>
    where
        E: serde::de::Error,
    {
        self.delegate.visit_char(v)
    }

    fn visit_str<E>(self, v: &str) -> Result<Self::Value, E>
    where
        E: serde::de::Error,
    {
        self.delegate.visit_str(v)
    }

    fn visit_borrowed_str<E>(self, v: &'de str) -> Result<Self::Value, E>
    where
        E: serde::de::Error,
    {
        self.delegate.visit_borrowed_str(v)
    }

    fn visit_string<E>(self, v: String) -> Result<Self::Value, E>
    where
        E: serde::de::Error,
    {
        self.delegate.visit_string(v)
    }

    fn visit_unit<E>(self) -> Result<Self::Value, E>
    where
        E: serde::de::Error,
    {
        self.delegate.visit_unit()
    }

    fn visit_none<E>(self) -> Result<Self::Value, E>
    where
        E: serde::de::Error,
    {
        self.delegate.visit_none()
    }

    fn visit_some<D>(self, deserializer: D) -> Result<Self::Value, D::Error>
    where
        D: serde::de::Deserializer<'de>,
    {
        self.delegate.visit_some(Deserializer {
            de: deserializer,
            names: self.names,
        })
    }

    fn visit_newtype_struct<D>(self, deserializer: D) -> Result<Self::Value, D::Error>
    where
        D: serde::de::Deserializer<'de>,
    {
        self.delegate.visit_newtype_struct(Deserializer {
            de: deserializer,
            names: self.names,
        })
    }

    fn visit_seq<V>(self, visitor: V) -> Result<Self::Value, V::Error>
    where
        V: serde::de::SeqAccess<'de>,
    {
        self.delegate.visit_seq(Wrap {
            delegate: visitor,
            names: self.names,
        })
    }

    fn visit_map<V>(self, visitor: V) -> Result<Self::Value, V::Error>
    where
        V: serde::de::MapAccess<'de>,
    {
        self.delegate.visit_map(Wrap {
            delegate: visitor,
            names: self.names,
        })
    }

    fn visit_enum<V>(self, visitor: V) -> Result<Self::Value, V::Error>
    where
        V: serde::de::EnumAccess<'de>,
    {
        self.delegate.visit_enum(Wrap {
            delegate: visitor,
            names: self.names,
        })
    }

    fn visit_bytes<E>(self, v: &[u8]) -> Result<Self::Value, E>
    where
        E: serde::de::Error,
    {
        self.delegate.visit_bytes(v)
    }

    fn visit_borrowed_bytes<E>(self, v: &'de [u8]) -> Result<Self::Value, E>
    where
        E: serde::de::Error,
    {
        self.delegate.visit_borrowed_bytes(v)
    }

    fn visit_byte_buf<E>(self, v: Vec<u8>) -> Result<Self::Value, E>
    where
        E: serde::de::Error,
    {
        self.delegate.visit_byte_buf(v)
    }
}

impl<'a, 'de, X> serde::de::EnumAccess<'de> for Wrap<'a, X>
where
    X: serde::de::EnumAccess<'de>,
{
    type Error = X::Error;
    type Variant = Wrap<'a, X::Variant>;

    fn variant_seed<V>(self, seed: V) -> Result<(V::Value, Self::Variant), X::Error>
    where
        V: serde::de::DeserializeSeed<'de>,
    {
        self.delegate
            .variant_seed(Wrap {
                delegate: seed,
                names: self.names,
            })
            .map(|(v, vis)| {
                (
                    v,
                    Wrap {
                        delegate: vis,
                        names: self.names,
                    },
                )
            })
    }
}

impl<'de, X> serde::de::VariantAccess<'de> for Wrap<'_, X>
where
    X: serde::de::VariantAccess<'de>,
{
    type Error = X::Error;

    fn unit_variant(self) -> Result<(), X::Error> {
        self.delegate.unit_variant()
    }

    fn newtype_variant_seed<T>(self, seed: T) -> Result<T::Value, X::Error>
    where
        T: serde::de::DeserializeSeed<'de>,
    {
        self.delegate.newtype_variant_seed(Wrap {
            delegate: seed,
            names: self.names,
        })
    }

    fn tuple_variant<V>(self, len: usize, visitor: V) -> Result<V::Value, X::Error>
    where
        V: serde::de::Visitor<'de>,
    {
        self.delegate.tuple_variant(
            len,
            Wrap {
                delegate: visitor,
                names: self.names,
            },
        )
    }

    fn struct_variant<V>(
        self,
        fields: &'static [&'static str],
        visitor: V,
    ) -> Result<V::Value, X::Error>
    where
        V: serde::de::Visitor<'de>,
    {
        self.delegate.struct_variant(
            fields,
            Wrap {
                delegate: visitor,
                names: self.names,
            },
        )
    }
}

impl<'de, X> serde::de::SeqAccess<'de> for Wrap<'_, X>
where
    X: serde::de::SeqAccess<'de>,
{
    type Error = X::Error;

    fn next_element_seed<T>(&mut self, seed: T) -> Result<Option<T::Value>, X::Error>
    where
        T: serde::de::DeserializeSeed<'de>,
    {
        self.delegate.next_element_seed(Wrap {
            delegate: seed,
            names: self.names,
        })
    }

    fn size_hint(&self) -> Option<usize> {
        self.delegate.size_hint()
    }
}

impl<'de, X> serde::de::MapAccess<'de> for Wrap<'_, X>
where
    X: serde::de::MapAccess<'de>,
{
    type Error = X::Error;

    fn next_key_seed<K>(&mut self, seed: K) -> Result<Option<K::Value>, X::Error>
    where
        K: serde::de::DeserializeSeed<'de>,
    {
        self.delegate.next_key_seed(Wrap {
            delegate: seed,
            names: self.names,
        })
    }

    fn next_value_seed<V>(&mut self, seed: V) -> Result<V::Value, X::Error>
    where
        V: serde::de::DeserializeSeed<'de>,
    {
        self.delegate.next_value_seed(Wrap {
            delegate: seed,
            names: self.names,
        })
    }

    fn size_hint(&self) -> Option<usize> {
        self.delegate.size_hint()
    }
}

impl<'de, X> serde::de::DeserializeSeed<'de> for Wrap<'_, X>
where
    X: serde::de::DeserializeSeed<'de>,
{
    type Value = X::Value;

    fn deserialize<D>(self, deserializer: D) -> Result<Self::Value, D::Error>
    where
        D: serde::de::Deserializer<'de>,
    {
        self.delegate.deserialize(Deserializer {
            de: deserializer,
            names: self.names,
        })
    }
}
