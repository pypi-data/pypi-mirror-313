use std::{
    borrow::Cow,
    collections::HashSet,
    fs::File,
    hash::{Hash, Hasher},
    io::{self, BufRead, Write},
    path::{Path, PathBuf},
};

use bloomfilter::Bloom;
use uuid::Uuid;

use core_compressor::compressor::ConcreteCompressor;
use core_dataset::{dataset::Dataset, variable::DataVariable};
use core_error::LocationError;

pub struct BenchmarkCase<'a> {
    pub dataset: &'a Dataset,
    pub variable: &'a DataVariable,
    pub compressor: Cow<'a, ConcreteCompressor<'a>>,
}

impl BenchmarkCase<'_> {
    #[must_use]
    pub fn get_id(&self) -> BenchmarkCaseId {
        BenchmarkCaseId::new(self)
    }

    #[must_use]
    pub fn get_uuid(&self) -> Uuid {
        self.get_id().into_uuid()
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct BenchmarkCaseId {
    dataset: u32,
    variable: u16,
    compressor: u16,
    codec_params: u32,
    checksum: u32,
}

impl BenchmarkCaseId {
    #[must_use]
    pub fn new(case: &BenchmarkCase) -> Self {
        let dataset = case.dataset.config_path().map_or(0, Self::hash_dataset);
        let variable = Self::hash_variable(case.variable.name());
        let compressor = case
            .compressor
            .config_path()
            // we need to re-insert the UUIDv8 version number if we fall-back
            .map_or(0b1000_u16 << 12, Self::hash_compressor);
        let codec_params = Self::hash_codec_params(&case.compressor);

        let mut checksum = fnv::FnvHasher::default();
        case.dataset.config_path().hash(&mut checksum);
        case.dataset.path().hash(&mut checksum);
        case.dataset.format().hash(&mut checksum);
        case.variable.name().hash(&mut checksum);
        case.variable.long_name().hash(&mut checksum);
        case.variable.dtype().hash(&mut checksum);
        case.variable.units().hash(&mut checksum);
        case.variable.dimensions().count().hash(&mut checksum);
        case.variable
            .dimensions()
            .for_each(|(name, _)| name.hash(&mut checksum));
        case.compressor.config_path().hash(&mut checksum);
        case.compressor.name().hash(&mut checksum);
        case.compressor.codecs().len().hash(&mut checksum);
        case.compressor.codecs().for_each(|codec| {
            codec.import_path().as_str().hash(&mut checksum);
            codec.kind().hash(&mut checksum);
            codec.parameters().count().hash(&mut checksum);
            codec.parameters().for_each(|(name, param)| {
                name.hash(&mut checksum);
                param.hash(&mut checksum);
            });
        });
        #[expect(clippy::cast_possible_truncation)]
        let checksum = (checksum.finish() & u64::from(u32::MAX)) as u32;

        Self {
            dataset,
            variable,
            compressor,
            codec_params,
            checksum,
        }
    }

    #[must_use]
    pub const fn from_uuid(uuid: Uuid) -> Self {
        let bytes = uuid.into_bytes();

        let mut checksum_bytes = [0u8; 4];
        checksum_bytes[0] = bytes[12];
        checksum_bytes[1] = bytes[13];
        checksum_bytes[2] = bytes[14];
        checksum_bytes[3] = bytes[15];
        let checksum = u32::from_be_bytes(checksum_bytes);

        let mut dataset_bytes = [0u8; 4];
        dataset_bytes[0] = bytes[0] ^ checksum_bytes[0];
        dataset_bytes[1] = bytes[1] ^ checksum_bytes[1];
        dataset_bytes[2] = bytes[2] ^ checksum_bytes[2];
        dataset_bytes[3] = bytes[3] ^ checksum_bytes[3];
        let dataset = u32::from_be_bytes(dataset_bytes);

        let mut variable_bytes = [0u8; 2];
        variable_bytes[0] = bytes[4] ^ checksum_bytes[0];
        variable_bytes[1] = bytes[5] ^ checksum_bytes[1];
        let variable = u16::from_be_bytes(variable_bytes);

        let mut compressor_bytes = [0u8; 2];
        compressor_bytes[0] = bytes[6] ^ (checksum_bytes[2] & (u8::MAX >> 4));
        compressor_bytes[1] = bytes[7] ^ checksum_bytes[3];
        let compressor = u16::from_be_bytes(compressor_bytes);

        let mut codec_params_bytes = [0u8; 4];
        codec_params_bytes[0] = bytes[8] ^ (checksum_bytes[0] & (u8::MAX >> 2));
        codec_params_bytes[1] = bytes[9] ^ checksum_bytes[1];
        codec_params_bytes[2] = bytes[10] ^ checksum_bytes[2];
        codec_params_bytes[3] = bytes[11] ^ checksum_bytes[3];
        let codec_params = u32::from_be_bytes(codec_params_bytes);

        Self {
            dataset,
            variable,
            compressor,
            codec_params,
            checksum,
        }
    }

    #[must_use]
    pub fn into_uuid(self) -> Uuid {
        let mut bytes = [0u8; 16];

        let checksum_bytes = self.checksum.to_be_bytes();

        let dataset_bytes = self.dataset.to_be_bytes();
        bytes[0] = dataset_bytes[0] ^ checksum_bytes[0];
        bytes[1] = dataset_bytes[1] ^ checksum_bytes[1];
        bytes[2] = dataset_bytes[2] ^ checksum_bytes[2];
        bytes[3] = dataset_bytes[3] ^ checksum_bytes[3];

        let variable_bytes = self.variable.to_be_bytes();
        bytes[4] = variable_bytes[0] ^ checksum_bytes[0];
        bytes[5] = variable_bytes[1] ^ checksum_bytes[1];

        let compressor_bytes = self.compressor.to_be_bytes();
        bytes[6] = compressor_bytes[0] ^ (checksum_bytes[2] & (u8::MAX >> 4));
        bytes[7] = compressor_bytes[1] ^ checksum_bytes[3];

        let codec_params_bytes = self.codec_params.to_be_bytes();
        bytes[8] = codec_params_bytes[0] ^ (checksum_bytes[0] & (u8::MAX >> 2));
        bytes[9] = codec_params_bytes[1] ^ checksum_bytes[1];
        bytes[10] = codec_params_bytes[2] ^ checksum_bytes[2];
        bytes[11] = codec_params_bytes[3] ^ checksum_bytes[3];

        bytes[12] = checksum_bytes[0];
        bytes[13] = checksum_bytes[1];
        bytes[14] = checksum_bytes[2];
        bytes[15] = checksum_bytes[3];

        Uuid::new_v8(bytes)
    }

    fn hash_dataset(dataset: &Path) -> u32 {
        let mut hasher = fnv::FnvHasher::default();
        dataset.hash(&mut hasher);
        #[expect(clippy::cast_possible_truncation)]
        let hash = (hasher.finish() & u64::from(u32::MAX)) as u32;
        hash
    }

    fn hash_variable(variable: &str) -> u16 {
        let mut hasher = fnv::FnvHasher::default();
        variable.hash(&mut hasher);
        #[expect(clippy::cast_possible_truncation)]
        let hash = (hasher.finish() & u64::from(u16::MAX)) as u16;
        hash
    }

    fn hash_compressor(compressor: &Path) -> u16 {
        let mut hasher = fnv::FnvHasher::default();
        compressor.hash(&mut hasher);
        #[expect(clippy::cast_possible_truncation)]
        let hash = (hasher.finish() & u64::from(u16::MAX)) as u16;
        // include UUIDv8 version field
        (hash & (u16::MAX >> 4)) | (0b1000_u16 << 12)
    }

    fn hash_codec_params(concrete_compressor: &ConcreteCompressor) -> u32 {
        let mut hasher = fnv::FnvHasher::default();
        concrete_compressor.codecs().for_each(|codec| {
            codec.parameters().for_each(|(_, param)| {
                param.hash(&mut hasher);
            });
        });
        #[expect(clippy::cast_possible_truncation)]
        let hash = (hasher.finish() & u64::from(u32::MAX)) as u32;
        // include UUIDv8 variant field
        (hash & (u32::MAX >> 2)) | (0b10_u32 << 30)
    }
}

impl serde::Serialize for BenchmarkCaseId {
    fn serialize<S: serde::Serializer>(&self, serializer: S) -> Result<S::Ok, S::Error> {
        serde::Serializer::serialize_newtype_struct(
            serializer,
            "BenchmarkCaseId",
            &self.into_uuid(),
        )
    }
}

impl<'de> serde::Deserialize<'de> for BenchmarkCaseId {
    fn deserialize<D: serde::Deserializer<'de>>(deserializer: D) -> Result<Self, D::Error> {
        struct Visitor;

        impl<'de> serde::de::Visitor<'de> for Visitor {
            type Value = BenchmarkCaseId;

            fn expecting(&self, fmt: &mut std::fmt::Formatter) -> std::fmt::Result {
                fmt.write_str("newtype struct BenchmarkCaseIdUuid")
            }

            #[inline]
            fn visit_newtype_struct<D: serde::Deserializer<'de>>(
                self,
                deserializer: D,
            ) -> Result<Self::Value, D::Error> {
                let uuid = <Uuid as serde::Deserialize>::deserialize(deserializer)?;
                Ok(BenchmarkCaseId::from_uuid(uuid))
            }
        }

        serde::Deserializer::deserialize_newtype_struct(deserializer, "BenchmarkCaseId", Visitor)
    }
}

#[derive(Copy, Clone, serde::Serialize, serde::Deserialize)]
#[serde(rename = "BenchmarkCaseId")]
struct BenchmarkCaseIdUuid(Uuid);

pub struct BenchmarkCaseFilter {
    ids: HashSet<BenchmarkCaseId>,
    dataset: Bloom<u32>,
    variable: Bloom<u16>,
    compressor: Bloom<u16>,
    codec_params: Bloom<u32>,
}

#[derive(Debug, thiserror::Error)]
pub enum BenchmarkCaseFilterError {
    #[error("failed to construct a bloom filter")]
    BloomFilter(BloomFilterError),
    #[error("failed to load case filter from {path:?}")]
    LoadFromFile { path: PathBuf, source: io::Error },
    #[error("failed to read case UUID")]
    InvalidCaseUuid { source: uuid::Error },
    #[error("failed to write case filter to {path:?}")]
    WriteToFile { path: PathBuf, source: io::Error },
}

#[derive(Debug, thiserror::Error)]
#[error("{0}")]
pub struct BloomFilterError(&'static str);

impl BenchmarkCaseFilter {
    pub fn new(
        case_ids: HashSet<BenchmarkCaseId>,
    ) -> Result<Self, LocationError<BenchmarkCaseFilterError>> {
        fn new_inner(
            case_ids: HashSet<BenchmarkCaseId>,
        ) -> Result<BenchmarkCaseFilter, &'static str> {
            const FP_RATE: f64 = 0.001_f64;

            let mut dataset = Bloom::new_for_fp_rate(case_ids.len(), FP_RATE)?;
            let mut variable = Bloom::new_for_fp_rate(case_ids.len(), FP_RATE)?;
            let mut compressor = Bloom::new_for_fp_rate(case_ids.len(), FP_RATE)?;
            let mut codec_params = Bloom::new_for_fp_rate(case_ids.len(), FP_RATE)?;

            for id in &case_ids {
                dataset.set(&id.dataset);
                variable.set(&id.variable);
                compressor.set(&id.compressor);
                codec_params.set(&id.codec_params);
            }

            Ok(BenchmarkCaseFilter {
                ids: case_ids,
                dataset,
                variable,
                compressor,
                codec_params,
            })
        }

        new_inner(case_ids).map_err(|err| {
            LocationError::new(BenchmarkCaseFilterError::BloomFilter(BloomFilterError(err)))
        })
    }

    pub fn load_from_file(path: &Path) -> Result<Self, LocationError<BenchmarkCaseFilterError>> {
        let file = File::open(path).map_err(|err| BenchmarkCaseFilterError::LoadFromFile {
            path: path.to_path_buf(),
            source: err,
        })?;

        let mut case_ids = HashSet::new();

        for line in io::BufReader::new(file).lines() {
            let line = line.map_err(|err| BenchmarkCaseFilterError::LoadFromFile {
                path: path.to_path_buf(),
                source: err,
            })?;
            let uuid = Uuid::parse_str(&line)
                .map_err(|err| BenchmarkCaseFilterError::InvalidCaseUuid { source: err })?;
            case_ids.insert(BenchmarkCaseId::from_uuid(uuid));
        }

        Self::new(case_ids)
    }

    pub fn write_ids_to_file(
        case_ids: &HashSet<BenchmarkCaseId>,
        path: &Path,
    ) -> Result<(), LocationError<BenchmarkCaseFilterError>> {
        fn write_ids_to_file_inner(
            case_ids: &HashSet<BenchmarkCaseId>,
            path: &Path,
        ) -> Result<(), LocationError<io::Error>> {
            let file = File::options().create_new(true).write(true).open(path)?;

            let mut writer = io::BufWriter::new(file);

            for id in case_ids {
                writeln!(writer, "{}", BenchmarkCaseId::into_uuid(*id))?;
            }

            writer.flush()?;

            Ok(())
        }

        write_ids_to_file_inner(case_ids, path).map_err(|err| {
            err.map(|err| BenchmarkCaseFilterError::WriteToFile {
                path: path.to_path_buf(),
                source: err,
            })
        })
    }

    #[must_use]
    pub fn is_empty(&self) -> bool {
        self.ids.is_empty()
    }

    #[must_use]
    pub fn len(&self) -> usize {
        self.ids.len()
    }

    #[must_use]
    pub fn contains_dataset(&self, dataset: &Path) -> bool {
        self.dataset.check(&BenchmarkCaseId::hash_dataset(dataset))
    }

    #[must_use]
    pub fn contains_variable(&self, variable: &str) -> bool {
        self.variable
            .check(&BenchmarkCaseId::hash_variable(variable))
    }

    #[must_use]
    pub fn contains_compressor(&self, compressor: &Path) -> bool {
        self.compressor
            .check(&BenchmarkCaseId::hash_compressor(compressor))
    }

    #[must_use]
    pub fn contains_codec_params(&self, codec_params: &ConcreteCompressor) -> bool {
        self.codec_params
            .check(&BenchmarkCaseId::hash_codec_params(codec_params))
    }

    #[must_use]
    pub fn contains_case(&self, case: &BenchmarkCase) -> bool {
        self.ids.contains(&case.get_id())
    }

    #[must_use]
    pub fn contains_case_id(&self, id: &BenchmarkCaseId) -> bool {
        self.ids.contains(id)
    }

    #[must_use]
    pub fn iter(&self) -> impl ExactSizeIterator<Item = BenchmarkCaseId> + '_ {
        self.ids.iter().copied()
    }
}

impl IntoIterator for BenchmarkCaseFilter {
    type IntoIter = <HashSet<BenchmarkCaseId> as IntoIterator>::IntoIter;
    type Item = BenchmarkCaseId;

    fn into_iter(self) -> Self::IntoIter {
        self.ids.into_iter()
    }
}

#[cfg(test)]
mod tests {
    use super::BenchmarkCaseId;

    #[test]
    fn check_case_id_roundtrip() {
        let id = BenchmarkCaseId {
            dataset: 0,
            variable: 9_703,
            compressor: 32_768,
            codec_params: 2_463_485_636,
            checksum: 1_475_811_263,
        };
        let uuid = id.into_uuid();
        let id2 = BenchmarkCaseId::from_uuid(uuid);
        assert_eq!(id, id2);
    }
}
