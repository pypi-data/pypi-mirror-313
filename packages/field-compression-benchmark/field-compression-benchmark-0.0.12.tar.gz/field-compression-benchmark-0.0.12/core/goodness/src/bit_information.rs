use std::{convert::Infallible, fmt, ops::IndexMut};

use numpy::{
    Element, PyArray1, PyArrayDescrMethods, PyArrayMethods, PyUntypedArray, PyUntypedArrayMethods,
};
use pyo3::{exceptions::PyTypeError, intern, prelude::*};

use core_error::LocationError;
use core_measure::Measurement;

pub enum DataArrayBitInformation {}

impl DataArrayBitInformation {
    pub fn goodness<'py>(
        py: Python<'py>,
        da_raw: Borrowed<'_, 'py, PyAny>,
        da_compressed: Borrowed<'_, 'py, PyAny>,
        set_zero_insignificant_confidence: Option<f64>,
    ) -> Result<BitInformationGoodness, LocationError<PyErr>> {
        let information_content_raw =
            Self::information_content(py, da_raw, set_zero_insignificant_confidence)?;
        let information_content_compressed =
            Self::information_content(py, da_compressed, set_zero_insignificant_confidence)?;

        Ok(BitInformationGoodness::new(
            information_content_compressed / information_content_raw,
        ))
    }

    pub fn bit_information<'py>(
        py: Python<'py>,
        da: Borrowed<'_, 'py, PyAny>,
        set_zero_insignificant_confidence: Option<f64>,
    ) -> Result<Bound<'py, PyArray1<f64>>, LocationError<PyErr>> {
        Self::bit_information_array(
            py,
            da.getattr(intern!(py, "values"))?
                .extract::<Bound<PyUntypedArray>>()?
                .as_borrowed(),
            set_zero_insignificant_confidence,
        )
    }

    pub fn bit_information_array<'py>(
        py: Python<'py>,
        a: Borrowed<'_, 'py, PyUntypedArray>,
        set_zero_insignificant_confidence: Option<f64>,
    ) -> Result<Bound<'py, PyArray1<f64>>, LocationError<PyErr>> {
        fn bit_information_typed<'py, T: BitInformationElement + Element>(
            data: Borrowed<'_, 'py, PyArray1<T>>,
            set_zero_insignificant_confidence: Option<f64>,
        ) -> Result<Bound<'py, PyArray1<f64>>, LocationError<PyErr>> {
            let readonly_data = (*data).try_readonly().map_err(PyErr::from)?;
            let data_slice = readonly_data.as_slice().map_err(PyErr::from)?;

            let bit_information = DataArrayBitInformation::bit_information_slice(
                data_slice,
                set_zero_insignificant_confidence,
            );

            Ok(PyArray1::from_slice(data.py(), bit_information.as_ref()))
        }

        let flattened_values: Bound<PyUntypedArray> =
            a.call_method0(intern!(py, "ravel"))?.extract()?;

        let dtype = flattened_values.dtype();

        if dtype.is_equiv_to(&numpy::dtype::<f32>(py)) {
            bit_information_typed(
                flattened_values
                    .downcast::<PyArray1<f32>>()
                    .map_err(PyErr::from)?
                    .as_borrowed(),
                set_zero_insignificant_confidence,
            )
        } else if dtype.is_equiv_to(&numpy::dtype::<f64>(py)) {
            bit_information_typed(
                flattened_values
                    .downcast::<PyArray1<f64>>()
                    .map_err(PyErr::from)?
                    .as_borrowed(),
                set_zero_insignificant_confidence,
            )
        } else if dtype.is_equiv_to(&numpy::dtype::<u32>(py)) {
            bit_information_typed(
                flattened_values
                    .downcast::<PyArray1<u32>>()
                    .map_err(PyErr::from)?
                    .as_borrowed(),
                set_zero_insignificant_confidence,
            )
        } else if dtype.is_equiv_to(&numpy::dtype::<u64>(py)) {
            bit_information_typed(
                flattened_values
                    .downcast::<PyArray1<u64>>()
                    .map_err(PyErr::from)?
                    .as_borrowed(),
                set_zero_insignificant_confidence,
            )
        } else {
            Err(PyTypeError::new_err(format!(
                "Unsupported dtype: {dtype}, information_content currently only supports float32, \
                 float64, uint32, and uint64"
            ))
            .into())
        }
    }

    pub fn information_content<'py>(
        py: Python<'py>,
        da: Borrowed<'_, 'py, PyAny>,
        set_zero_insignificant_confidence: Option<f64>,
    ) -> Result<f64, LocationError<PyErr>> {
        Self::information_content_array(
            py,
            da.getattr(intern!(py, "values"))?
                .extract::<Bound<PyUntypedArray>>()?
                .as_borrowed(),
            set_zero_insignificant_confidence,
        )
    }

    pub fn information_content_array<'py>(
        py: Python<'py>,
        a: Borrowed<'_, 'py, PyUntypedArray>,
        set_zero_insignificant_confidence: Option<f64>,
    ) -> Result<f64, LocationError<PyErr>> {
        fn information_content_typed<T: BitInformationElement + Element>(
            data: Borrowed<PyArray1<T>>,
            set_zero_insignificant_confidence: Option<f64>,
        ) -> Result<f64, LocationError<PyErr>> {
            let readonly_data = (*data).try_readonly().map_err(PyErr::from)?;
            let data_slice = readonly_data.as_slice().map_err(PyErr::from)?;

            let bit_information = DataArrayBitInformation::bit_information_slice(
                data_slice,
                set_zero_insignificant_confidence,
            );

            let information_content = bit_information.as_ref().iter().sum();

            Ok(information_content)
        }

        let flattened_values: Bound<PyUntypedArray> =
            a.call_method0(intern!(py, "ravel"))?.extract()?;

        let dtype = flattened_values.dtype();

        if dtype.is_equiv_to(&numpy::dtype::<f32>(py)) {
            information_content_typed(
                flattened_values
                    .downcast::<PyArray1<f32>>()
                    .map_err(PyErr::from)?
                    .as_borrowed(),
                set_zero_insignificant_confidence,
            )
        } else if dtype.is_equiv_to(&numpy::dtype::<f64>(py)) {
            information_content_typed(
                flattened_values
                    .downcast::<PyArray1<f64>>()
                    .map_err(PyErr::from)?
                    .as_borrowed(),
                set_zero_insignificant_confidence,
            )
        } else if dtype.is_equiv_to(&numpy::dtype::<u32>(py)) {
            information_content_typed(
                flattened_values
                    .downcast::<PyArray1<u32>>()
                    .map_err(PyErr::from)?
                    .as_borrowed(),
                set_zero_insignificant_confidence,
            )
        } else if dtype.is_equiv_to(&numpy::dtype::<u64>(py)) {
            information_content_typed(
                flattened_values
                    .downcast::<PyArray1<u64>>()
                    .map_err(PyErr::from)?
                    .as_borrowed(),
                set_zero_insignificant_confidence,
            )
        } else {
            Err(PyTypeError::new_err(format!(
                "Unsupported dtype: {dtype}, information_content currently only supports float32, \
                 float64, uint32, and uint64"
            ))
            .into())
        }
    }

    pub fn required_bits<'py>(
        py: Python<'py>,
        da: Borrowed<'_, 'py, PyAny>,
        information_ratio: f64,
        set_zero_insignificant_confidence: Option<f64>,
    ) -> Result<usize, LocationError<PyErr>> {
        Self::required_bits_array(
            py,
            da.getattr(intern!(py, "values"))?
                .extract::<Bound<PyUntypedArray>>()?
                .as_borrowed(),
            information_ratio,
            set_zero_insignificant_confidence,
        )
    }

    pub fn required_bits_array<'py>(
        py: Python<'py>,
        a: Borrowed<'_, 'py, PyUntypedArray>,
        information_ratio: f64,
        set_zero_insignificant_confidence: Option<f64>,
    ) -> Result<usize, LocationError<PyErr>> {
        fn required_bits_typed<T: BitInformationElement + Element>(
            data: Borrowed<PyArray1<T>>,
            information_ratio: f64,
            set_zero_insignificant_confidence: Option<f64>,
        ) -> Result<usize, LocationError<PyErr>> {
            let readonly_data = (*data).try_readonly().map_err(PyErr::from)?;
            let data_slice = readonly_data.as_slice().map_err(PyErr::from)?;

            let required_bits = DataArrayBitInformation::required_bits_slice(
                data_slice,
                information_ratio,
                set_zero_insignificant_confidence,
            );

            Ok(required_bits)
        }

        let flattened_values: Bound<PyUntypedArray> =
            a.call_method0(intern!(py, "ravel"))?.extract()?;

        let dtype = flattened_values.dtype();

        if dtype.is_equiv_to(&numpy::dtype::<f32>(py)) {
            required_bits_typed(
                flattened_values
                    .downcast::<PyArray1<f32>>()
                    .map_err(PyErr::from)?
                    .as_borrowed(),
                information_ratio,
                set_zero_insignificant_confidence,
            )
        } else if dtype.is_equiv_to(&numpy::dtype::<f64>(py)) {
            required_bits_typed(
                flattened_values
                    .downcast::<PyArray1<f64>>()
                    .map_err(PyErr::from)?
                    .as_borrowed(),
                information_ratio,
                set_zero_insignificant_confidence,
            )
        } else if dtype.is_equiv_to(&numpy::dtype::<u32>(py)) {
            required_bits_typed(
                flattened_values
                    .downcast::<PyArray1<u32>>()
                    .map_err(PyErr::from)?
                    .as_borrowed(),
                information_ratio,
                set_zero_insignificant_confidence,
            )
        } else if dtype.is_equiv_to(&numpy::dtype::<u64>(py)) {
            required_bits_typed(
                flattened_values
                    .downcast::<PyArray1<u64>>()
                    .map_err(PyErr::from)?
                    .as_borrowed(),
                information_ratio,
                set_zero_insignificant_confidence,
            )
        } else {
            Err(PyTypeError::new_err(format!(
                "Unsupported dtype: {dtype}, required_bits currently only supports float32, \
                 float64, uint32, and uint64"
            ))
            .into())
        }
    }

    pub fn required_bits_slice<T: BitInformationElement>(
        data: &[T],
        information_ratio: f64,
        set_zero_insignificant_confidence: Option<f64>,
    ) -> usize {
        let bit_information = Self::bit_information_slice(data, set_zero_insignificant_confidence);
        let bit_information = bit_information.as_ref();

        let total_information: f64 = bit_information.iter().sum();
        if total_information <= f64::EPSILON {
            return 0;
        }

        bit_information
            .iter()
            .scan(0.0_f64, |state, i| {
                if (*state / total_information) >= information_ratio {
                    return None;
                }

                *state += *i;

                Some(())
            })
            .count()
    }

    pub fn bit_information_slice<T: BitInformationElement>(
        data: &[T],
        set_zero_insignificant_confidence: Option<f64>,
    ) -> T::NBitArray<f64> {
        let ([front @ .., _], [_, back @ ..]) = (data, data) else {
            // no data elements -> every bit has zero information
            return T::fill(0.0_f64);
        };

        if front.is_empty() {
            // only one element -> every bit has full information
            return T::fill(1.0_f64);
        }

        #[expect(clippy::cast_precision_loss)]
        let n_elements = front.len() as f64;

        let bitpair_counter = Self::bitpair_count(front, back);

        let mut mutual_information = T::map(bitpair_counter, |bitpair_counter| {
            let mut joint_probability_mass_function = [[0.0_f64, 0.0_f64], [0.0_f64, 0.0_f64]];

            crunchy::unroll! { for j in 0..2 {
                crunchy::unroll! { for k in 0..2 {
                    #[expect(clippy::cast_precision_loss)]
                    {
                        joint_probability_mass_function[j][k] =
                            (bitpair_counter[j][k] as f64) / n_elements;
                    }
                } }
            } }

            Self::binary_mutual_information_of_joint_probability_mass_function(
                joint_probability_mass_function,
            )
        });

        if let Some(insignificant_confidence) = set_zero_insignificant_confidence {
            Self::set_zero_insignificant(
                mutual_information.as_mut(),
                front.len(),
                insignificant_confidence,
            );
        }

        mutual_information
    }

    fn bitpair_count<T: BitInformationElement>(
        front: &[T],
        back: &[T],
    ) -> T::NBitArray<[[usize; 2]; 2]> {
        let mut bitpair_counter = T::fill([[0, 0], [0, 0]]);

        for (a, b) in front.iter().zip(back.iter()) {
            // count the bits and update counter array C
            Self::bitpair_count_scalar(&mut bitpair_counter, a, b);
        }

        bitpair_counter
    }

    fn bitpair_count_scalar<T: BitInformationElement>(
        bitpair_counter: &mut T::NBitArray<[[usize; 2]; 2]>,
        a: &T,
        b: &T,
    ) {
        // loop from least to most significant bit
        for bi in 0..T::NBITS {
            // isolate that bit in a and b, so that j and k are either 0b0 or 0b1
            let j = a.extract_bit(bi);
            let k = b.extract_bit(bi);

            // increase the bit pair's counter
            // all indices are in bounds, but clippy cannot see it for j and k
            //  and we cannot prove it for bi since T::NBitArray doesn't expose
            //  that its length is guaranteed to be T::NBITS
            #[expect(clippy::indexing_slicing)]
            {
                bitpair_counter[T::NBITS - bi - 1][usize::from(j)][usize::from(k)] += 1;
            }
        }
    }

    fn binary_mutual_information_of_joint_probability_mass_function(
        // events X are 1st dim, Y is 2nd
        joint_probability_mass_function: [[f64; 2]; 2],
    ) -> f64 {
        let p = joint_probability_mass_function;

        // Entries in p have to sum to 1
        assert!((p[0][0] + p[0][1] + p[1][0] + p[1][1] - 1.0).abs() <= f64::EPSILON);
        // Entries in p have to be non-negative
        assert!(p[0][0] >= 0.0);
        assert!(p[0][1] >= 0.0);
        assert!(p[1][0] >= 0.0);
        assert!(p[1][1] >= 0.0);

        // marginal probabilities of y
        let py = [p[0][0] + p[1][0], p[0][1] + p[1][1]];
        // marginal probabilities of x
        let px = [p[0][0] + p[0][1], p[1][0] + p[1][1]];

        let mut mutual_information = 0.0;

        crunchy::unroll! { for j in 0..2 {
            crunchy::unroll! { for i in 0..2 {
                // add binary entropy only for non-zero entries in p
                if p[i][j] > 0.0 {
                    mutual_information += p[i][j] * (p[i][j] / px[i] / py[j]).log2();
                }
            } }
        } }

        mutual_information
    }

    fn set_zero_insignificant(mutual_information: &mut [f64], n_elements: usize, confidence: f64) {
        let free_entropy_of_50_50 = Self::binom_free_binary_entropy(n_elements, confidence);

        for h in mutual_information {
            if *h <= free_entropy_of_50_50 {
                *h = 0.0;
            }
        }
    }

    fn binom_free_binary_entropy(n: usize, confidence: f64) -> f64 {
        let p = Self::binom_confidence(n, confidence);

        let binary_entropy = -p.mul_add(p.log2(), (1.0 - p) * (1.0 - p).log2());

        1.0 - binary_entropy
    }

    fn binom_confidence(n: usize, confidence: f64) -> f64 {
        #[expect(clippy::cast_precision_loss)]
        let n = n as f64;

        let p = 0.5
            + Self::standard_normal_quantile((1.0 - confidence).mul_add(-0.5, 1.0))
                / (n.sqrt() * 2.0);

        // cap probability at 1 (only important for when n is small)
        p.min(1.0_f64)
    }

    fn standard_normal_quantile(p: f64) -> f64 {
        std::f64::consts::SQRT_2 * puruspe::inverf(p.mul_add(2.0, -1.0))
    }
}

#[derive(Copy, Clone, Debug, PartialEq, serde::Serialize, serde::Deserialize)]
#[serde(deny_unknown_fields)]
pub struct BitInformationGoodness {
    information_content_ratio: f64,
}

impl BitInformationGoodness {
    #[must_use]
    pub const fn new(information_content_ratio: f64) -> Self {
        Self {
            information_content_ratio,
        }
    }
}

impl Measurement for BitInformationGoodness {
    type Error = Infallible;

    fn to_f64(&self) -> f64 {
        self.information_content_ratio
    }

    fn try_from_f64(information_content_ratio: f64) -> Result<Self, LocationError<Self::Error>> {
        Ok(Self {
            information_content_ratio,
        })
    }

    fn fmt(&self, fmt: &mut fmt::Formatter) -> fmt::Result {
        fmt.write_fmt(format_args!(
            "{:.2}%",
            self.information_content_ratio * 100.0
        ))
    }
}

pub trait BitInformationElement {
    type NBitArray<T>: AsRef<[T]> + AsMut<[T]> + IndexMut<usize, Output = T>;

    const NBITS: usize;

    fn map<T, O>(a: Self::NBitArray<T>, f: impl FnMut(T) -> O) -> Self::NBitArray<O>;
    fn fill<T: Copy>(x: T) -> Self::NBitArray<T>;

    fn extract_bit(&self, bit: usize) -> bool;
}

impl BitInformationElement for u32 {
    type NBitArray<T> = [T; Self::NBITS];

    const NBITS: usize = Self::BITS as usize;

    fn fill<T: Copy>(x: T) -> Self::NBitArray<T> {
        [x; Self::NBITS]
    }

    fn map<T, O>(a: Self::NBitArray<T>, f: impl FnMut(T) -> O) -> Self::NBitArray<O> {
        a.map(f)
    }

    fn extract_bit(&self, bit: usize) -> bool {
        ((*self >> bit) & 1) == 1
    }
}

impl BitInformationElement for u64 {
    type NBitArray<T> = [T; Self::NBITS];

    const NBITS: usize = Self::BITS as usize;

    fn fill<T: Copy>(x: T) -> Self::NBitArray<T> {
        [x; Self::NBITS]
    }

    fn map<T, O>(a: Self::NBitArray<T>, f: impl FnMut(T) -> O) -> Self::NBitArray<O> {
        a.map(f)
    }

    fn extract_bit(&self, bit: usize) -> bool {
        ((*self >> bit) & 1) == 1
    }
}

impl BitInformationElement for f32 {
    type NBitArray<T> = [T; Self::NBITS];

    const NBITS: usize = u32::BITS as usize;

    fn fill<T: Copy>(x: T) -> Self::NBitArray<T> {
        [x; Self::NBITS]
    }

    fn map<T, O>(a: Self::NBitArray<T>, f: impl FnMut(T) -> O) -> Self::NBitArray<O> {
        a.map(f)
    }

    fn extract_bit(&self, bit: usize) -> bool {
        (((*self).to_bits() >> bit) & 1) == 1
    }
}

impl BitInformationElement for f64 {
    type NBitArray<T> = [T; Self::NBITS];

    const NBITS: usize = u64::BITS as usize;

    fn fill<T: Copy>(x: T) -> Self::NBitArray<T> {
        [x; Self::NBITS]
    }

    fn map<T, O>(a: Self::NBitArray<T>, f: impl FnMut(T) -> O) -> Self::NBitArray<O> {
        a.map(f)
    }

    fn extract_bit(&self, bit: usize) -> bool {
        (((*self).to_bits() >> bit) & 1) == 1
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn assert_close<const N: usize>(a: [f64; N], b: [f64; N]) {
        let close = a
            .iter()
            .zip(b.iter())
            .all(|(a, b)| (a - b).abs() <= f64::EPSILON);

        assert!(close, "{a:?} != {b:?}");
    }

    #[test]
    #[expect(clippy::cognitive_complexity)]
    fn bit_information_u32() {
        assert_close(
            DataArrayBitInformation::bit_information_slice(&[0_u32, 0], None),
            [0.0_f64; 32],
        );

        assert_close(
            DataArrayBitInformation::bit_information_slice(
                &(0..32).map(|i| 1_u32 << i).collect::<Vec<_>>(),
                None,
            ),
            {
                let mut bit_information = [0.0_f64; 32];
                crunchy::unroll! { for i in 1..31 {
                    bit_information[i] = 0.001_551_572_392_955_275;
                } }
                bit_information
            },
        );
    }

    #[test]
    #[expect(clippy::cognitive_complexity)]
    fn bit_information_u64() {
        assert_close(
            DataArrayBitInformation::bit_information_slice(&[0_u64, 0], None),
            [0.0_f64; 64],
        );

        assert_close(
            DataArrayBitInformation::bit_information_slice(
                &(0..64).map(|i| 1_u64 << i).collect::<Vec<_>>(),
                None,
            ),
            {
                let mut bit_information = [0.0_f64; 64];
                crunchy::unroll! { for i in 1..63 {
                    bit_information[i] = 0.000_369_369_585_051_767_4;
                } }
                bit_information
            },
        );
    }

    #[test]
    fn bit_information_f32() {
        assert_close(
            DataArrayBitInformation::bit_information_slice(&[1.0_f32, 1.0], None),
            [0.0_f64; 32],
        );

        assert_close(
            DataArrayBitInformation::bit_information_slice(&[1.0_f32, 2.0, 3.0, 4.0], None),
            {
                let mut bit_information = [0.0_f64; 32];
                bit_information[8] = 0.251_629_167_387_822_8;
                bit_information[9] = 0.251_629_167_387_822_8;
                bit_information
            },
        );
    }

    #[test]
    fn bit_information_f64() {
        assert_close(
            DataArrayBitInformation::bit_information_slice(&[1.0, 1.0], None),
            [0.0_f64; 64],
        );

        assert_close(
            DataArrayBitInformation::bit_information_slice(&[1.0, 2.0, 3.0, 4.0], None),
            {
                let mut bit_information = [0.0_f64; 64];
                bit_information[11] = 0.251_629_167_387_822_8;
                bit_information[12] = 0.251_629_167_387_822_8;
                bit_information
            },
        );
    }
}
