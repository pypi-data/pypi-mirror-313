use std::{
    fs, io,
    num::NonZeroUsize,
    path::{Path, PathBuf},
};

use byte_unit::Byte;
use clap::{Args, ColorChoice, Parser, Subcommand, ValueEnum};
use log::LevelFilter;
use vecmap::VecSet;

use core_error::LocationError;

pub struct Cli {
    pub command: Command,
    /// Level of log messages which are printed to stderr
    pub log: Option<LogLevelFilter>,
    /// Disable any messages to be printed to stdout or stderr
    pub quiet: bool,
    /// Colour and pretty-format console messages
    pub color: Option<ColorChoice>,
}

pub enum Command {
    /// Execute the benchmarking suite
    Bench(BenchArgs),
    /// Launch the embedded Python REPL
    Python(PythonArgs),
}

pub struct BenchArgs {
    /// Include the following WASM codec files
    pub codecs: VecSet<PathBuf>,
    /// Include the following compressor config files
    pub compressors: VecSet<PathBuf>,
    /// Include the following dataset config files
    pub datasets: VecSet<PathBuf>,
    /// Store the line-separated list of case UUIDs to this file (with
    /// --dry-run)  or load the list of case UUIDs from this file (with
    /// --no-dry-run)
    pub cases: Option<PathBuf>,
    /// Don't actually run any benchmark; just check all inputs
    pub dry_run: bool,
    /// Repeat each benchmark case several times to collect multiple
    /// measurements
    pub num_repeats: NonZeroUsize,
    /// Seed the random number generator used for bootstrap analysis,
    /// or use a random seed
    pub bootstrap_seed: Option<u64>,
    /// Resample all measurements with replacement to generate bootstrapping
    /// statistics
    pub bootstrap_samples: Option<NonZeroUsize>,
    /// Number of bins in the compression error histogram
    pub error_bins: NonZeroUsize,
    /// Resample the compression error distribution at regular intervals
    pub error_resamples: NonZeroUsize,
    /// Maximum number of PCA modes that are computed for the preserved PCA
    /// goodness score
    pub pca_max_modes: NonZeroUsize,
    /// Default chunk size for automatic chunking of datasets
    pub dataset_auto_chunk_size: Byte,
    /// Store the results to a JSON report file
    pub output: Option<PathBuf>,
    /// Resume the benchmark from an existing JSON report file
    pub resume: bool,
    /// Only benchmark the smallest subset of benchmark dimension
    pub minimal: Minimal,
    /// Keep going when a benchmark case fails
    pub keep_going: bool,
    /// Distribute the benchmark across several processes, or use the available
    /// parallelism
    pub num_processes: Option<NonZeroUsize>,
    /// Select the detail of the progress updates as benchmark cases complete
    pub progress: Option<Progress>,
}

pub struct PythonArgs {
    /// Program read from script file
    pub file: Option<PathBuf>,
    /// Arguments passed to the program in sys.argv\[1:\]
    pub arg: Vec<String>,
}

impl Cli {
    pub fn parse() -> Result<Self, LocationError<io::Error>> {
        let CliImpl {
            command,
            log,
            quiet,
            color,
        } = CliImpl::parse();

        let command = match command {
            CommandImpl::Bench(args) => {
                let BenchArgsImpl {
                    codecs,
                    excluded_codecs,
                    compressors,
                    excluded_compressors,
                    datasets,
                    excluded_datasets,
                    cases,
                    minimal,
                    dry_run,
                    num_repeats,
                    bootstrap_seed,
                    bootstrap_samples,
                    error_bins,
                    error_resamples,
                    pca_max_modes,
                    dataset_auto_chunk_size,
                    output,
                    resume,
                    keep_going,
                    num_processes,
                    progress,
                    _no_dry_run,
                    _no_resume,
                    _no_keep_going,
                } = *args;

                let args = BenchArgs {
                    codecs: CliImpl::expand_exclude_config_files(
                        &codecs,
                        &excluded_codecs,
                        "wasm",
                    )?,
                    compressors: CliImpl::expand_exclude_config_files(
                        &compressors,
                        &excluded_compressors,
                        "toml",
                    )?,
                    datasets: CliImpl::expand_exclude_config_files(
                        &datasets,
                        &excluded_datasets,
                        "toml",
                    )?,
                    cases,
                    minimal: Minimal::from(minimal),
                    dry_run,
                    num_repeats,
                    bootstrap_seed,
                    bootstrap_samples: NonZeroUsize::new(bootstrap_samples),
                    error_bins,
                    error_resamples,
                    pca_max_modes,
                    dataset_auto_chunk_size,
                    output,
                    resume,
                    keep_going,
                    num_processes,
                    progress,
                };

                Command::Bench(args)
            },
            CommandImpl::Python(args) => {
                let PythonArgsImpl { file, arg } = *args;

                Command::Python(PythonArgs { file, arg })
            },
            CommandImpl::MarkdownHelp => {
                let markdown = clap_markdown::help_markdown::<CliImpl>();

                // insert extra newlines before list items where necessary
                let mut markdown_fixed = String::with_capacity(markdown.len());
                let mut last_newline = false;
                for line in markdown.lines() {
                    if last_newline && line.is_empty() {
                        continue;
                    }
                    if line.trim_start().starts_with(['*', '-']) && !last_newline {
                        markdown_fixed.push('\n');
                    }
                    last_newline = line.is_empty();
                    markdown_fixed.push_str(line);
                    markdown_fixed.push('\n');
                }

                println!("{markdown_fixed}");
                std::process::exit(0); // success
            },
        };

        Ok(Self {
            command,
            log,
            quiet,
            color,
        })
    }
}

#[expect(clippy::doc_markdown)]
/// ESiWACE3 data compression benchmarking suite
///
/// The suite compares the performance of various data compression methods with
/// different settings across a variety of variables and their derivatives from
/// different GRIB, NetCDF, or Zarr datasets.
#[derive(Parser)]
#[command(author, version, about, long_about)]
#[command(help_template = "\
{before-help}{name} v{version}
  by {author}

{about}

{usage-heading} {usage}

{all-args}{after-help}")]
struct CliImpl {
    #[command(subcommand)]
    command: CommandImpl,

    /// Level of log messages which are printed to stderr
    #[arg(short, long, value_enum, conflicts_with = "quiet")]
    log: Option<LogLevelFilter>,

    /// Disable any messages to be printed to stdout or stderr
    #[arg(short, long)]
    quiet: bool,

    /// Colour and pretty-format console messages
    #[arg(short, long, value_enum)]
    color: Option<ColorChoice>,
}

#[derive(Subcommand)]
enum CommandImpl {
    /// Execute the benchmarking suite
    Bench(Box<BenchArgsImpl>),
    /// Launch the embedded Python REPL
    Python(Box<PythonArgsImpl>),
    #[command(hide = true)]
    /// Print help, formatted as Markdown
    MarkdownHelp,
}

#[expect(clippy::struct_excessive_bools)]
#[derive(Args)]
struct BenchArgsImpl {
    /// Include the following WASM codec files or directories
    #[arg(long = "codec", num_args(0..), default_value = Path::new("data").join("codecs").into_os_string())]
    codecs: Vec<PathBuf>,

    /// Exclude the following WASM codec files or directories
    #[arg(long = "exclude-codecs", num_args(0..))]
    excluded_codecs: Vec<PathBuf>,

    /// Include the following compressor config files or directories
    #[arg(long = "compressor", num_args(0..), default_value = Path::new("data").join("compressors").into_os_string())]
    compressors: Vec<PathBuf>,

    /// Exclude the following compressor config files or directories
    #[arg(long = "exclude-compressor", num_args(0..))]
    excluded_compressors: Vec<PathBuf>,

    /// Include the following dataset config files or directories
    #[arg(long = "dataset", num_args(0..), default_value = Path::new("data").join("datasets").into_os_string())]
    datasets: Vec<PathBuf>,

    /// Exclude the following dataset config files or directories
    #[arg(long = "exclude-dataset", num_args(0..))]
    excluded_datasets: Vec<PathBuf>,

    /// Store the line-separated list of case UUIDs to this file (with
    /// --dry-run)  or load the list of case UUIDs from this file (with
    /// --no-dry-run)
    #[arg(short, long)]
    cases: Option<PathBuf>,

    /// Only benchmark the smallest subset of benchmark dimension
    #[arg(short, long, num_args(0..), value_enum)]
    minimal: Option<Vec<MinimalFlag>>,

    /// Don't actually run any benchmark; just check all inputs
    #[arg(short, long, conflicts_with = "output", overrides_with = "_no_dry_run")]
    dry_run: bool,

    /// Repeat each benchmark case several times to collect multiple
    /// measurements
    #[arg(short, long, default_value = "10")]
    num_repeats: NonZeroUsize,

    /// Seed the random number generator used for bootstrap analysis,
    /// or use a random seed
    #[arg(short = 's', long)]
    bootstrap_seed: Option<u64>,

    /// Resample all measurements with replacement to generate bootstrapping
    /// statistics
    #[arg(short = 'b', long, default_value = "1000")]
    bootstrap_samples: usize,

    /// Maximum number of PCA modes that are computed for the preserved PCA
    /// goodness score
    #[arg(long, default_value = "10")]
    pca_max_modes: NonZeroUsize,

    /// Number of bins in the compression error histogram
    #[arg(long, default_value = "100")]
    error_bins: NonZeroUsize,

    /// Resample the compression error distribution at regular intervals
    #[arg(long, default_value = "100")]
    error_resamples: NonZeroUsize,

    /// Default chunk size for automatic chunking of datasets
    #[arg(long, default_value = "32 MiB")]
    dataset_auto_chunk_size: Byte,

    /// Store the results to a JSON report file
    #[arg(short, long)]
    output: Option<PathBuf>,

    /// Resume the benchmark from an existing JSON report file
    #[arg(long, requires = "output", overrides_with = "_no_resume")]
    resume: bool,

    /// Keep going when a benchmark case fails
    #[arg(short, long, overrides_with = "_no_keep_going")]
    keep_going: bool,

    /// Distribute the benchmark across several processes, or use the available
    /// parallelism
    #[arg(short = 'p', long)]
    num_processes: Option<NonZeroUsize>,

    /// Select the detail of the progress updates as benchmark cases complete
    #[arg(long)]
    progress: Option<Progress>,

    /// Execute all benchmark cases (default)
    #[arg(long = "no-dry-run")]
    _no_dry_run: bool,

    /// Create a fresh JSON report file, do not resume from one (default)
    #[arg(long = "no-resume", requires = "output")]
    _no_resume: bool,

    /// Stop with the first benchmark case failure (default)
    #[arg(long = "no-keep-going")]
    _no_keep_going: bool,
}

#[derive(Args)]
#[clap(trailing_var_arg = true)]
struct PythonArgsImpl {
    /// Program read from script file
    file: Option<PathBuf>,
    /// Arguments passed to the program in sys.argv\[1:\]
    #[clap(num_args(0..), allow_hyphen_values=true)]
    arg: Vec<String>,
}

impl CliImpl {
    fn expand_exclude_config_files(
        includes: &[PathBuf],
        excludes: &[PathBuf],
        extension: &str,
    ) -> Result<VecSet<PathBuf>, LocationError<io::Error>> {
        let mut expanded = VecSet::with_capacity(includes.len());

        for path in includes {
            if path.is_dir() {
                for path in fs::read_dir(path)? {
                    let path = path?.path();
                    if matches!(path.extension(), Some(ext) if ext == extension) {
                        expanded.insert(path);
                    }
                }
            } else if path.is_file() {
                expanded.insert(path.clone());
            }
        }

        for path in excludes {
            if path.is_dir() {
                for path in fs::read_dir(path)? {
                    let path = path?.path();
                    if matches!(path.extension(), Some(ext) if ext == extension) {
                        expanded.remove(&path);
                    }
                }
            } else if path.is_file() {
                expanded.remove(path);
            }
        }

        Ok(expanded)
    }
}

#[expect(clippy::struct_excessive_bools)]
pub struct Minimal {
    pub codec_parameters: bool,
    pub dataset_variables: bool,
    pub variable_dimensions: bool,
    pub variable_derivatives: bool,
}

impl From<Option<Vec<MinimalFlag>>> for Minimal {
    fn from(flags: Option<Vec<MinimalFlag>>) -> Self {
        let Some(flags) = flags else {
            return Self {
                codec_parameters: false,
                dataset_variables: false,
                variable_dimensions: false,
                variable_derivatives: false,
            };
        };

        if flags.is_empty() || flags.contains(&MinimalFlag::All) {
            return Self {
                codec_parameters: true,
                dataset_variables: true,
                variable_dimensions: true,
                variable_derivatives: true,
            };
        }

        Self {
            codec_parameters: flags.contains(&MinimalFlag::CodecParameters),
            dataset_variables: flags.contains(&MinimalFlag::DatasetVariables),
            variable_dimensions: flags.contains(&MinimalFlag::VariableDimensions),
            variable_derivatives: flags.contains(&MinimalFlag::VariableDerivatives),
        }
    }
}

#[derive(Clone, Debug, PartialEq, Eq, ValueEnum)]
enum MinimalFlag {
    All,
    CodecParameters,
    DatasetVariables,
    VariableDimensions,
    VariableDerivatives,
}

#[derive(Clone, Debug, ValueEnum)]
pub enum LogLevelFilter {
    Off,
    Error,
    Warn,
    Info,
    Debug,
    Trace,
}

impl From<LogLevelFilter> for LevelFilter {
    fn from(filter: LogLevelFilter) -> Self {
        match filter {
            LogLevelFilter::Off => Self::Off,
            LogLevelFilter::Error => Self::Error,
            LogLevelFilter::Warn => Self::Warn,
            LogLevelFilter::Info => Self::Info,
            LogLevelFilter::Debug => Self::Debug,
            LogLevelFilter::Trace => Self::Trace,
        }
    }
}

#[derive(Clone, Debug, ValueEnum)]
pub enum Progress {
    Off,
    Minimal,
    Report,
}
