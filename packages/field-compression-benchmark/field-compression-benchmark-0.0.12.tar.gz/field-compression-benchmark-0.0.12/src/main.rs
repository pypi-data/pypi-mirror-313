use std::{
    borrow::Cow,
    collections::HashSet,
    ffi::CString,
    iter::FusedIterator,
    num::NonZeroUsize,
    path::{Path, PathBuf},
    sync::Mutex,
};

use args::PythonArgs;
use byte_unit::{Byte, Unit, UnitType};
use clap::ColorChoice;
use log::LevelFilter;
use pretty_env_logger::env_logger::WriteStyle;
use pyo3::{exceptions::PySystemExit, prelude::*, types::PyList};
use pyo3_error::PyErrChain;
use thiserror::Error;
use vecmap::VecSet;

use codecs_build as _;
use core_benchmark::{
    case::{BenchmarkCase, BenchmarkCaseFilter, BenchmarkCaseFilterError, BenchmarkCaseId},
    report::BenchmarkReport,
    settings::{
        BenchmarkSettings, BootstrapSettings, ErrorSettings, MeasurementSettings, MetricsSettings,
        PCASettings,
    },
};
use core_dataset::dataset::{Dataset, DatasetSettings};
use core_error::{pyerr_chain_from_location_err, pyerr_from_location_err, LocationError};
use fork::Reaper;

mod args;
mod benchmarking;
mod codecs;

use crate::{
    args::{Cli, Command, Progress},
    benchmarking::{
        prepare::{Benchmark, BenchmarkPrepareError},
        report::JsonReporter,
        run_benchmark,
    },
};

#[allow(clippy::missing_errors_doc)] // FIXME, expect does not used
pub fn main() -> anyhow::Result<()> {
    // use anyhow for formatting the error report
    main_cli().map_err(anyhow::Error::new)
}

#[expect(clippy::missing_errors_doc, clippy::too_many_lines)] // FIXME
pub fn main_cli() -> Result<(), LocationError<BenchmarkSuiteError>> {
    let Cli {
        command,
        log,
        quiet,
        color,
    } = Cli::parse().map_err(BenchmarkSuiteError::CliArgs)?;

    // create a Python runtime
    pyo3::prepare_freethreaded_python();

    let args = match command {
        Command::Bench(args) => args,
        Command::Python(PythonArgs { file: None, arg: _ }) => return python_repl(),
        Command::Python(PythonArgs {
            file: Some(file),
            arg,
        }) => return python_exec(&file, arg),
    };

    setup_log_and_color(log.map(LevelFilter::from), quiet, color)?;

    let token = try_get_reaper_token(&fork::REAPER_TOKEN).map_err(BenchmarkSuiteError::Reaper)?;

    Reaper::with_subprocess_reaper(token, |reaper| {
        Python::with_gil(|py| {
            Benchmark::prepare_python(py)
                .map_err(|err| err.map(|err| pyerr_chain_from_location_err(py, err)))
                .map_err(BenchmarkSuiteError::PythonDependencies)
        })?;

        let settings = prepare_benchmark_settings(
            args.num_repeats,
            args.bootstrap_seed,
            args.bootstrap_samples,
            args.error_resamples,
            args.error_bins,
            args.pca_max_modes,
            args.dataset_auto_chunk_size,
        )
        .map_err(BenchmarkSuiteError::BenchmarkSettings)?;

        Python::with_gil(|py| {
            codecs::import_fcbench_codecs(py, args.codecs)
                .map_err(|err| err.map(|err| pyerr_chain_from_location_err(py, err)))
                .map_err(BenchmarkSuiteError::FcpyCodecs)
        })?;

        let case_filter = match args.cases.as_ref() {
            Some(cases) if !args.dry_run => Some(
                BenchmarkCaseFilter::load_from_file(cases)
                    .map_err(BenchmarkSuiteError::CaseIdFile)?,
            ),
            Some(_) | None => None,
        };

        let benchmark = Python::with_gil(|py| {
            Benchmark::prepare(
                py,
                args.compressors,
                args.datasets,
                &args.minimal,
                case_filter.as_ref(),
                &settings.datasets,
            )
        })
        .map_err(BenchmarkSuiteError::PrepareBenchmark)?;

        let num_compressors = Python::with_gil(|py| {
            benchmark.pre_check_concrete_compressors(py, case_filter.as_ref())
        })
        .map_err(LocationError::from)
        .map_err(BenchmarkSuiteError::PrepareBenchmark)?;

        let benchmark_cases = generate_benchmark_cases(&benchmark, &case_filter);

        if args.dry_run {
            let benchmark_case_ids: HashSet<BenchmarkCaseId> =
                benchmark_cases.map(|case| case.get_id()).collect();

            println!("- Finished dry run of {} case(s)", benchmark_case_ids.len());

            if let Some(cases) = args.cases {
                BenchmarkCaseFilter::write_ids_to_file(&benchmark_case_ids, &cases)
                    .map_err(BenchmarkSuiteError::CaseIdFile)?;
                println!("- Saved line-separated benchmark case IDs to {cases:?}");
            }

            return Ok(());
        }

        let num_processes = match args.num_processes {
            Some(num_processes) => num_processes,
            None => {
                std::thread::available_parallelism().map_err(BenchmarkSuiteError::Parallelism)?
            },
        };

        let num_dataset_variables = benchmark
            .datasets()
            .map(|dataset: &Dataset| dataset.variables().len())
            .sum::<usize>();
        let num_cases = num_compressors * num_dataset_variables;

        let report = run_benchmark_with_reporters(
            reaper,
            benchmark_cases,
            settings,
            ReporterSettings {
                num_processes,
                quiet,
                keep_going: args.keep_going,
                output: args.output,
                resume: args.resume,
                progress: args.progress,
            },
            case_filter.as_ref(),
            num_cases,
        )?;

        println!();

        if report.summary.cancelled > 0 {
            println!(
                "The benchmark exited early with {} successful, {} failed, and {} cancelled \
                 case(s).",
                report.summary.success, report.summary.failures, report.summary.cancelled
            );
        } else {
            println!(
                "The benchmark completed with {} successful and {} failed case(s).",
                report.summary.success, report.summary.failures
            );
        }

        Ok(())
    })
}

fn python_repl() -> Result<(), LocationError<BenchmarkSuiteError>> {
    Python::with_gil(|py| {
        (|| -> Result<(), LocationError<PyErr>> {
            let sys = py.import("sys")?;
            let sys_version: String = sys.getattr("version")?.extract()?;
            let sys_platform: String = sys.getattr("platform")?.extract()?;

            let banner = format!(
                "Python {sys_version} on {sys_platform}\nType \"help\", \"copyright\", \
                 \"credits\" or \"license\" for more information."
            );

            let Err(err) = py
                .import("code")?
                .getattr("interact")?
                .call1((banner,))
                .map_err(LocationError::new)
            else {
                return Ok(());
            };

            if !err.error().is_instance_of::<PySystemExit>(py) {
                return Err(err);
            }

            let code = err.error().value(py).getattr("code")?;

            if code.is_none() {
                return Ok(());
            }

            if let Ok(code) = code.extract() {
                std::process::exit(code);
            }

            err.error().print(py);
            std::process::exit(1);
        })()
        .map_err(|err| err.map(|err| pyerr_chain_from_location_err(py, err)))
    })
    .map_err(|err| LocationError::new(BenchmarkSuiteError::Repl(err)))
}

#[allow(clippy::similar_names)] // file_str and file_cstr
fn python_exec(
    file: &Path,
    mut args: Vec<String>,
) -> Result<(), LocationError<BenchmarkSuiteError>> {
    Python::with_gil(|py| {
        (|| -> Result<(), LocationError<PyErr>> {
            let code = std::fs::read(file).map_err(|err| {
                let err = anyhow::Error::new(err).context(format!("can't open file {file:?}"));
                pyerr_from_location_err(py, err)
            })?;
            let code = CString::new(code).map_err(|err| {
                let err =
                    anyhow::Error::new(err).context(format!("file {file:?} contains null byte(s)"));
                pyerr_from_location_err(py, err)
            })?;

            let file_str = file.display().to_string();

            args.insert(0, file_str.clone());
            let args = PyList::new(py, args)?;

            let sys = py.import("sys")?;
            sys.setattr("argv", args)?;

            let file_cstr = CString::new(file_str.into_bytes()).map_err(|err| {
                let err = anyhow::Error::new(err)
                    .context(format!("filepath {file:?} contains null byte(s)"));
                pyerr_from_location_err(py, err)
            })?;

            let _module = PyModule::from_code(py, &code, &file_cstr, c"__main__")?;

            Ok(())
        })()
        .map_err(|err| err.map(|err| pyerr_chain_from_location_err(py, err)))
    })
    .map_err(|err| LocationError::new(BenchmarkSuiteError::Repl(err)))
}

fn try_get_reaper_token<T>(token: &Mutex<Option<T>>) -> Result<T, LocationError<ReaperError>> {
    match token.lock().map(|mut guarded_token| guarded_token.take()) {
        Ok(Some(token)) => Ok(token),
        Ok(None) => Err(ReaperError::AlreadyInitialised.into()),
        Err(_) => Err(ReaperError::PoisonedToken.into()),
    }
}

fn prepare_benchmark_settings(
    num_repeats: NonZeroUsize,
    bootstrap_seed: Option<u64>,
    bootstrap_samples: Option<NonZeroUsize>,
    error_resamples: NonZeroUsize,
    error_bins: NonZeroUsize,
    pca_max_modes: NonZeroUsize,
    dataset_auto_chunk_size: Byte,
) -> Result<BenchmarkSettings, LocationError<getrandom::Error>> {
    println!("Benchmark configuration:");
    println!("- Number of repeats: {num_repeats}");

    println!("- Measurement bootstrapping:");

    let bootstrap_seed = if let Some(seed) = bootstrap_seed {
        println!("  - seed: {seed}");
        seed
    } else {
        let mut bytes = [0_u8; std::mem::size_of::<u64>()];
        getrandom::getrandom(&mut bytes)?;
        let seed = u64::from_ne_bytes(bytes);
        println!("  - seed: {seed} (random)");
        seed
    };

    println!(
        "  - number of resamples: {}",
        bootstrap_samples.map_or(0, NonZeroUsize::get)
    );

    println!("- Error distribution intervals: {error_resamples}");
    println!(
        "- Default dataset auto chunk size: {} ({})",
        dataset_auto_chunk_size.get_appropriate_unit(UnitType::Both),
        dataset_auto_chunk_size.get_adjusted_unit(Unit::B),
    );

    Ok(BenchmarkSettings {
        datasets: DatasetSettings {
            auto_chunk_size: dataset_auto_chunk_size,
        },
        measurements: MeasurementSettings {
            num_repeats,
            bootstrap: BootstrapSettings {
                seed: bootstrap_seed,
                samples: bootstrap_samples,
            },
            metrics: MetricsSettings {
                error: ErrorSettings {
                    bins: error_bins,
                    resamples: error_resamples,
                },
                pca: PCASettings {
                    max_modes: pca_max_modes,
                },
            },
        },
    })
}

#[allow(clippy::ref_option)] // case_filter lifetime only works with &Option
fn generate_benchmark_cases<'a>(
    benchmark: &'a Benchmark,
    case_filter: &'a Option<BenchmarkCaseFilter>,
) -> impl FusedIterator<Item = BenchmarkCase<'a>> + 'a {
    benchmark.datasets().flat_map(|dataset| {
        dataset.variables().flat_map(|variable| {
            benchmark
                .compressors()
                // we already pre-checked all configs,
                //  so we can silently skip errors here
                .filter_map(|compressor| compressor.iter_concrete().ok())
                .flat_map(|compressors| {
                    compressors
                        .filter_map(|codec_params| {
                            match codec_params {
                                Ok(codec_params)
                                    if case_filter.as_ref().map_or(true, |case_filter| {
                                        case_filter.contains_codec_params(&codec_params)
                                    }) =>
                                {
                                    Some(codec_params)
                                },
                                // we already pre-checked all configs,
                                //  so we can silently skip errors here
                                Ok(_) | Err(_) => None,
                            }
                        })
                        .map(|concrete| BenchmarkCase {
                            dataset,
                            variable,
                            compressor: Cow::Owned(concrete),
                        })
                        .filter(|case| {
                            case_filter
                                .as_ref()
                                .map_or(true, |case_filter| case_filter.contains_case(case))
                        })
                })
        })
    })
}

struct ReporterSettings {
    num_processes: NonZeroUsize,
    quiet: bool,
    keep_going: bool,
    output: Option<PathBuf>,
    resume: bool,
    progress: Option<Progress>,
}

fn run_benchmark_with_reporters<'a>(
    reaper: &Reaper,
    cases: impl FusedIterator<Item = BenchmarkCase<'a>>,
    settings: BenchmarkSettings,
    ReporterSettings {
        num_processes,
        quiet,
        keep_going,
        output,
        resume,
        progress,
    }: ReporterSettings,
    case_filter: Option<&BenchmarkCaseFilter>,
    num_cases: usize,
) -> Result<BenchmarkReport<'a>, LocationError<BenchmarkSuiteError>> {
    if let Some(case_filter) = case_filter.as_ref() {
        if case_filter.is_empty() {
            println!("- Benchmarking zero filtered cases");
        } else if case_filter.len() == num_cases {
            println!(
                "- Benchmarking ≤ {num_cases} fuzzy-filtered case(s) across {num_processes} \
                 processes:"
            );
        } else {
            println!(
                "- Benchmarking ≤ {} fuzzy-filtered case(s) across {num_processes} processes:",
                case_filter.len()
            );
        }
    } else {
        println!("- Benchmarking {num_cases} case(s) across {num_processes} processes:");
    }

    let mut reporters: Vec<&mut dyn core_benchmark::reporter::BenchmarkReporter> = vec![];
    let mut progress_reporter = benchmarking::report::ProgressReporter::new();
    if !quiet && matches!(progress, None | Some(Progress::Minimal | Progress::Report)) {
        reporters.push(&mut progress_reporter);
    }
    let mut minimal_reporter = benchmarking::report::MinimalErrorReporter;
    let mut verbose_reporter = benchmarking::report::VerboseConsoleReporter;
    let mut error_reporter = benchmarking::report::ErrorLogReporter;
    if !quiet {
        match progress {
            Some(Progress::Off) => {
                if log::max_level() >= LevelFilter::Error {
                    reporters.push(&mut error_reporter);
                }
            },
            Some(Progress::Minimal) => reporters.push(&mut minimal_reporter),
            None | Some(Progress::Report) => reporters.push(&mut verbose_reporter),
        }
    }
    let mut stop_error_reporter = core_benchmark::reporter::StopForError;
    if !keep_going {
        reporters.push(&mut stop_error_reporter);
    }
    let (mut json_reporter, completed_cases): (Option<JsonReporter>, VecSet<BenchmarkCaseId>) =
        if let Some(path) = output {
            if resume {
                let (json_reporter, completed_cases) = JsonReporter::resume(&path, &settings)
                    .map_err(JsonReporterError::Resume)
                    .map_err(BenchmarkSuiteError::JsonReporter)?;

                println!(
                    "  - Resuming with {} already completed case(s)",
                    completed_cases.len()
                );

                (Some(json_reporter), completed_cases)
            } else {
                let json_reporter = JsonReporter::create(&path, &settings)
                    .map_err(JsonReporterError::Create)
                    .map_err(BenchmarkSuiteError::JsonReporter)?;
                (Some(json_reporter), VecSet::new())
            }
        } else {
            (None, VecSet::new())
        };
    if let Some(json_reporter) = json_reporter.as_mut() {
        reporters.push(json_reporter);
    }

    let report = run_benchmark(
        reaper,
        cases.filter(|case| !completed_cases.contains(&case.get_id())),
        settings,
        num_processes,
        reporters.as_mut_slice(),
    );

    if let Some(json_reporter) = json_reporter.take() {
        json_reporter
            .finalise(&report.summary)
            .map_err(JsonReporterError::Save)
            .map_err(BenchmarkSuiteError::JsonReporter)?;
    }

    Ok(report)
}

fn setup_log_and_color(
    log: Option<LevelFilter>,
    quiet: bool,
    color: Option<ColorChoice>,
) -> Result<(), LocationError<BenchmarkSuiteError>> {
    const LOG_ENV_VAR: &str = "RUST_LOG";

    let no_color = std::env::var_os("NO_COLOR").map(|_| ());
    let cli_color_force = std::env::var_os("CLICOLOR_FORCE").map(|_| ());

    let color = match (color, no_color, cli_color_force) {
        (Some(color), _, _) => color,
        (None, Some(()), _) => ColorChoice::Never,
        (None, None, Some(())) => ColorChoice::Always,
        (None, None, None) => ColorChoice::Auto,
    };

    if let Some(log) = log {
        std::env::set_var(LOG_ENV_VAR, log.as_str());
    } else if std::env::var_os(LOG_ENV_VAR).is_none() {
        std::env::set_var(LOG_ENV_VAR, "warn");
    }

    let mut logger = pretty_env_logger::formatted_builder();
    if let Ok(filters) = std::env::var(LOG_ENV_VAR) {
        logger.parse_filters(&filters);
    }
    logger.write_style(match color {
        ColorChoice::Auto => WriteStyle::Auto,
        ColorChoice::Always => WriteStyle::Always,
        ColorChoice::Never => WriteStyle::Never,
    });
    logger.try_init().map_err(BenchmarkSuiteError::Logger)?;

    if quiet {
        let stdout_gag = gag::Gag::stdout().map_err(BenchmarkSuiteError::OutputGag)?;
        let stderr_gag = gag::Gag::stderr().map_err(BenchmarkSuiteError::OutputGag)?;

        Box::leak(Box::new(stdout_gag));
        Box::leak(Box::new(stderr_gag));
    }

    Ok(())
}

#[derive(Debug, Error)]
pub enum BenchmarkSuiteError {
    #[error("failed to parse the command line arguments")]
    CliArgs(#[source] LocationError<std::io::Error>),
    #[error("failed to run the Python REPL")]
    Repl(#[source] LocationError<PyErrChain>),
    #[error("failed to initialise the subprocess reaper")]
    Reaper(#[source] LocationError<ReaperError>),
    #[error("failed to load the Python dependencies")]
    PythonDependencies(#[source] LocationError<PyErrChain>),
    #[error("failed to initialise the benchmark settings")]
    BenchmarkSettings(#[source] LocationError<getrandom::Error>),
    #[error("failed to load the WASM codecs into fcpy")]
    FcpyCodecs(#[source] LocationError<PyErrChain>),
    #[error("failed to prepare the benchmark")]
    PrepareBenchmark(#[source] LocationError<BenchmarkPrepareError>),
    #[error(transparent)]
    CaseIdFile(LocationError<BenchmarkCaseFilterError>),
    #[error("failed to determine the available CPU parallelism")]
    Parallelism(#[source] std::io::Error),
    #[error(transparent)]
    JsonReporter(JsonReporterError),
    #[error("failed to initialise the logger")]
    Logger(#[source] log::SetLoggerError),
    #[error("failed to gag the stdout or stderr output")]
    OutputGag(#[source] std::io::Error),
}

#[derive(Debug, Error)]
pub enum ReaperError {
    #[error("the process reaper has already been initialised")]
    AlreadyInitialised,
    #[error("the process reaper has been poisoned")]
    PoisonedToken,
}

#[derive(Debug, Error)]
pub enum JsonReporterError {
    #[error("failed to create a new JSON report")]
    Create(#[source] LocationError<std::io::Error>),
    #[error("failed to resume from an existing JSON report")]
    Resume(#[source] LocationError<std::io::Error>),
    #[error("failed to save the the JSON report")]
    Save(#[source] LocationError<std::io::Error>),
}
