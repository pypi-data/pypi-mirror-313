// Adapted from David Tolnay's serde_path_to_error, which is "licensed under
// either of Apache License, Version 2.0 or MIT license at your option".
// https://github.com/dtolnay/path-to-error/blob/306187eee030e31ac0dc358f0b585c0f82b8a8d7/src/ser.rs

use std::{any::type_name, cell::RefCell, collections::HashMap};

pub struct Serialize<'a, T> {
    serialize: &'a T,
    names: &'a RefCell<HashMap<&'static str, &'static str>>,
}

impl<'a, T> Serialize<'a, T> {
    #[must_use]
    pub fn with<R>(
        serialize: &T,
        names: &'a mut HashMap<&'static str, &'static str>,
        inner: impl for<'b> FnOnce(&Serialize<'b, T>) -> R,
    ) -> R {
        let ref_cell_names = RefCell::new(std::mem::take(names));
        let result = inner(&Serialize {
            serialize,
            names: &ref_cell_names,
        });
        *names = ref_cell_names.into_inner();
        result
    }
}

impl<T: serde::ser::Serialize> serde::ser::Serialize for Serialize<'_, T> {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: serde::Serializer,
    {
        self.serialize.serialize(Serializer {
            ser: serializer,
            names: self.names,
            container_name: type_name::<T>(),
        })
    }
}

struct Serializer<'a, S> {
    ser: S,
    names: &'a RefCell<HashMap<&'static str, &'static str>>,
    container_name: &'static str,
}

struct Wrap<'a, X> {
    delegate: X,
    names: &'a RefCell<HashMap<&'static str, &'static str>>,
}

impl<'a, S> serde::ser::Serializer for Serializer<'a, S>
where
    S: serde::ser::Serializer,
{
    type Error = S::Error;
    type Ok = S::Ok;
    type SerializeMap = Wrap<'a, S::SerializeMap>;
    type SerializeSeq = Wrap<'a, S::SerializeSeq>;
    type SerializeStruct = Wrap<'a, S::SerializeStruct>;
    type SerializeStructVariant = Wrap<'a, S::SerializeStructVariant>;
    type SerializeTuple = Wrap<'a, S::SerializeTuple>;
    type SerializeTupleStruct = Wrap<'a, S::SerializeTupleStruct>;
    type SerializeTupleVariant = Wrap<'a, S::SerializeTupleVariant>;

    fn serialize_bool(self, v: bool) -> Result<Self::Ok, Self::Error> {
        self.ser.serialize_bool(v)
    }

    fn serialize_i8(self, v: i8) -> Result<Self::Ok, Self::Error> {
        self.ser.serialize_i8(v)
    }

    fn serialize_i16(self, v: i16) -> Result<Self::Ok, Self::Error> {
        self.ser.serialize_i16(v)
    }

    fn serialize_i32(self, v: i32) -> Result<Self::Ok, Self::Error> {
        self.ser.serialize_i32(v)
    }

    fn serialize_i64(self, v: i64) -> Result<Self::Ok, Self::Error> {
        self.ser.serialize_i64(v)
    }

    fn serialize_i128(self, v: i128) -> Result<Self::Ok, Self::Error> {
        self.ser.serialize_i128(v)
    }

    fn serialize_u8(self, v: u8) -> Result<Self::Ok, Self::Error> {
        self.ser.serialize_u8(v)
    }

    fn serialize_u16(self, v: u16) -> Result<Self::Ok, Self::Error> {
        self.ser.serialize_u16(v)
    }

    fn serialize_u32(self, v: u32) -> Result<Self::Ok, Self::Error> {
        self.ser.serialize_u32(v)
    }

    fn serialize_u64(self, v: u64) -> Result<Self::Ok, Self::Error> {
        self.ser.serialize_u64(v)
    }

    fn serialize_u128(self, v: u128) -> Result<Self::Ok, Self::Error> {
        self.ser.serialize_u128(v)
    }

    fn serialize_f32(self, v: f32) -> Result<Self::Ok, Self::Error> {
        self.ser.serialize_f32(v)
    }

    fn serialize_f64(self, v: f64) -> Result<Self::Ok, Self::Error> {
        self.ser.serialize_f64(v)
    }

    fn serialize_char(self, v: char) -> Result<Self::Ok, Self::Error> {
        self.ser.serialize_char(v)
    }

    fn serialize_str(self, v: &str) -> Result<Self::Ok, Self::Error> {
        self.ser.serialize_str(v)
    }

    fn serialize_bytes(self, v: &[u8]) -> Result<Self::Ok, Self::Error> {
        self.ser.serialize_bytes(v)
    }

    fn serialize_none(self) -> Result<Self::Ok, Self::Error> {
        self.ser.serialize_none()
    }

    fn serialize_some<T>(self, value: &T) -> Result<Self::Ok, Self::Error>
    where
        T: ?Sized + serde::ser::Serialize,
    {
        self.ser.serialize_some(&Wrap {
            delegate: value,
            names: self.names,
        })
    }

    fn serialize_unit(self) -> Result<Self::Ok, Self::Error> {
        self.ser.serialize_unit()
    }

    fn serialize_unit_struct(self, name: &'static str) -> Result<Self::Ok, Self::Error> {
        self.names.borrow_mut().insert(self.container_name, name);
        let name = self.container_name;

        self.ser.serialize_unit_struct(name)
    }

    fn serialize_unit_variant(
        self,
        name: &'static str,
        variant_index: u32,
        variant: &'static str,
    ) -> Result<Self::Ok, Self::Error> {
        self.names.borrow_mut().insert(self.container_name, name);
        let name = self.container_name;

        self.ser
            .serialize_unit_variant(name, variant_index, variant)
    }

    fn serialize_newtype_struct<T>(
        self,
        name: &'static str,
        value: &T,
    ) -> Result<Self::Ok, Self::Error>
    where
        T: ?Sized + serde::ser::Serialize,
    {
        self.names.borrow_mut().insert(self.container_name, name);
        let name = self.container_name;

        self.ser.serialize_newtype_struct(
            name,
            &Wrap {
                delegate: value,
                names: self.names,
            },
        )
    }

    fn serialize_newtype_variant<T>(
        self,
        name: &'static str,
        variant_index: u32,
        variant: &'static str,
        value: &T,
    ) -> Result<Self::Ok, Self::Error>
    where
        T: ?Sized + serde::ser::Serialize,
    {
        self.names.borrow_mut().insert(self.container_name, name);
        let name = self.container_name;

        self.ser.serialize_newtype_variant(
            name,
            variant_index,
            variant,
            &Wrap {
                delegate: value,
                names: self.names,
            },
        )
    }

    fn serialize_seq(self, len: Option<usize>) -> Result<Self::SerializeSeq, Self::Error> {
        self.ser.serialize_seq(len).map(|delegate| Wrap {
            delegate,
            names: self.names,
        })
    }

    fn serialize_tuple(self, len: usize) -> Result<Self::SerializeTuple, Self::Error> {
        self.ser.serialize_tuple(len).map(|delegate| Wrap {
            delegate,
            names: self.names,
        })
    }

    fn serialize_tuple_struct(
        self,
        name: &'static str,
        len: usize,
    ) -> Result<Self::SerializeTupleStruct, Self::Error> {
        self.names.borrow_mut().insert(self.container_name, name);
        let name = self.container_name;

        self.ser
            .serialize_tuple_struct(name, len)
            .map(|delegate| Wrap {
                delegate,
                names: self.names,
            })
    }

    fn serialize_tuple_variant(
        self,
        name: &'static str,
        variant_index: u32,
        variant: &'static str,
        len: usize,
    ) -> Result<Self::SerializeTupleVariant, Self::Error> {
        self.names.borrow_mut().insert(self.container_name, name);
        let name = self.container_name;

        self.ser
            .serialize_tuple_variant(name, variant_index, variant, len)
            .map(|delegate| Wrap {
                delegate,
                names: self.names,
            })
    }

    fn serialize_map(self, len: Option<usize>) -> Result<Self::SerializeMap, Self::Error> {
        self.ser.serialize_map(len).map(|delegate| Wrap {
            delegate,
            names: self.names,
        })
    }

    fn serialize_struct(
        self,
        name: &'static str,
        len: usize,
    ) -> Result<Self::SerializeStruct, Self::Error> {
        self.names.borrow_mut().insert(self.container_name, name);
        let name = self.container_name;

        self.ser.serialize_struct(name, len).map(|delegate| Wrap {
            delegate,
            names: self.names,
        })
    }

    fn serialize_struct_variant(
        self,
        name: &'static str,
        variant_index: u32,
        variant: &'static str,
        len: usize,
    ) -> Result<Self::SerializeStructVariant, Self::Error> {
        self.names.borrow_mut().insert(self.container_name, name);
        let name = self.container_name;

        self.ser
            .serialize_struct_variant(name, variant_index, variant, len)
            .map(|delegate| Wrap {
                delegate,
                names: self.names,
            })
    }

    fn collect_str<T>(self, value: &T) -> Result<Self::Ok, Self::Error>
    where
        T: ?Sized + std::fmt::Display,
    {
        self.ser.collect_str(value)
    }

    fn is_human_readable(&self) -> bool {
        self.ser.is_human_readable()
    }
}

impl<X> serde::ser::Serialize for Wrap<'_, X>
where
    X: serde::ser::Serialize,
{
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: serde::ser::Serializer,
    {
        self.delegate.serialize(Serializer {
            ser: serializer,
            names: self.names,
            container_name: type_name::<X>(),
        })
    }
}

impl<S> serde::ser::SerializeSeq for Wrap<'_, S>
where
    S: serde::ser::SerializeSeq,
{
    type Error = S::Error;
    type Ok = S::Ok;

    fn serialize_element<T>(&mut self, value: &T) -> Result<(), Self::Error>
    where
        T: ?Sized + serde::ser::Serialize,
    {
        self.delegate.serialize_element(&Wrap {
            delegate: value,
            names: self.names,
        })
    }

    fn end(self) -> Result<Self::Ok, Self::Error> {
        self.delegate.end()
    }
}

impl<S> serde::ser::SerializeTuple for Wrap<'_, S>
where
    S: serde::ser::SerializeTuple,
{
    type Error = S::Error;
    type Ok = S::Ok;

    fn serialize_element<T>(&mut self, value: &T) -> Result<(), Self::Error>
    where
        T: ?Sized + serde::ser::Serialize,
    {
        self.delegate.serialize_element(&Wrap {
            delegate: value,
            names: self.names,
        })
    }

    fn end(self) -> Result<Self::Ok, Self::Error> {
        self.delegate.end()
    }
}

impl<S> serde::ser::SerializeTupleStruct for Wrap<'_, S>
where
    S: serde::ser::SerializeTupleStruct,
{
    type Error = S::Error;
    type Ok = S::Ok;

    fn serialize_field<T>(&mut self, value: &T) -> Result<(), Self::Error>
    where
        T: ?Sized + serde::ser::Serialize,
    {
        self.delegate.serialize_field(&Wrap {
            delegate: value,
            names: self.names,
        })
    }

    fn end(self) -> Result<Self::Ok, Self::Error> {
        self.delegate.end()
    }
}

impl<S> serde::ser::SerializeTupleVariant for Wrap<'_, S>
where
    S: serde::ser::SerializeTupleVariant,
{
    type Error = S::Error;
    type Ok = S::Ok;

    fn serialize_field<T>(&mut self, value: &T) -> Result<(), Self::Error>
    where
        T: ?Sized + serde::ser::Serialize,
    {
        self.delegate.serialize_field(&Wrap {
            delegate: value,
            names: self.names,
        })
    }

    fn end(self) -> Result<Self::Ok, Self::Error> {
        self.delegate.end()
    }
}

impl<S> serde::ser::SerializeMap for Wrap<'_, S>
where
    S: serde::ser::SerializeMap,
{
    type Error = S::Error;
    type Ok = S::Ok;

    fn serialize_key<T>(&mut self, key: &T) -> Result<(), Self::Error>
    where
        T: ?Sized + serde::ser::Serialize,
    {
        self.delegate.serialize_key(&Wrap {
            delegate: key,
            names: self.names,
        })
    }

    fn serialize_value<T>(&mut self, value: &T) -> Result<(), Self::Error>
    where
        T: ?Sized + serde::ser::Serialize,
    {
        self.delegate.serialize_value(&Wrap {
            delegate: value,
            names: self.names,
        })
    }

    fn end(self) -> Result<Self::Ok, Self::Error> {
        self.delegate.end()
    }
}

impl<S> serde::ser::SerializeStruct for Wrap<'_, S>
where
    S: serde::ser::SerializeStruct,
{
    type Error = S::Error;
    type Ok = S::Ok;

    fn serialize_field<T>(&mut self, key: &'static str, value: &T) -> Result<(), Self::Error>
    where
        T: ?Sized + serde::ser::Serialize,
    {
        self.delegate.serialize_field(
            key,
            &Wrap {
                delegate: value,
                names: self.names,
            },
        )
    }

    fn end(self) -> Result<Self::Ok, Self::Error> {
        self.delegate.end()
    }

    fn skip_field(&mut self, key: &'static str) -> Result<(), Self::Error> {
        self.delegate.skip_field(key)
    }
}

impl<S> serde::ser::SerializeStructVariant for Wrap<'_, S>
where
    S: serde::ser::SerializeStructVariant,
{
    type Error = S::Error;
    type Ok = S::Ok;

    fn serialize_field<T>(&mut self, key: &'static str, value: &T) -> Result<(), Self::Error>
    where
        T: ?Sized + serde::ser::Serialize,
    {
        self.delegate.serialize_field(
            key,
            &Wrap {
                delegate: value,
                names: self.names,
            },
        )
    }

    fn end(self) -> Result<Self::Ok, Self::Error> {
        self.delegate.end()
    }

    fn skip_field(&mut self, key: &'static str) -> Result<(), Self::Error> {
        self.delegate.skip_field(key)
    }
}
