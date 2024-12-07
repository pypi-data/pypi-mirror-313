use std::{borrow::Cow, iter::FusedIterator, num::NonZeroUsize};

use fork::{distribute_work, Reaper};
use vecmap::VecMap;

use core_benchmark::{
    case::BenchmarkCase,
    error::{BenchmarkCaseError, StringifiedError},
    report::{BenchmarkCaseReport, BenchmarkReport, BenchmarkSummary},
    reporter::BenchmarkReporter,
    run_benchmark_case,
    settings::BenchmarkSettings,
};

pub mod prepare;
pub mod report;

pub fn run_benchmark<'a>(
    reaper: &Reaper,
    cases: impl FusedIterator<Item = BenchmarkCase<'a>>,
    settings: BenchmarkSettings,
    num_processes: NonZeroUsize,
    mut reporter: impl BenchmarkReporter,
) -> BenchmarkReport<'a> {
    let mut num_cases = 0;
    let mut cases = cases.inspect(|_| num_cases += 1);

    let mut success = 0;
    let mut failures = 0;
    let mut results = VecMap::new();

    let settings_clone = settings.clone();

    for (args, result) in distribute_work(
        reaper,
        move |BenchmarkCase {
                  dataset,
                  variable,
                  compressor,
              }| {
            log::debug!("Starting child benchmarking process");

            let result = pyo3::Python::with_gil(|py| {
                run_benchmark_case(py, dataset, variable, &compressor, &settings)
            })
            .map_err(BenchmarkCaseError::from);

            log::debug!("Finalising child benchmarking process");

            result
        },
        &mut cases,
        num_processes,
        false,
    ) {
        let (control, result) = match result {
            Ok(Ok(result)) => {
                success += 1;
                (reporter.report_success(&args, &result), Ok(result))
            },
            Ok(Err(err)) => {
                failures += 1;
                (reporter.report_error(&args, &err), Err(err))
            },
            Err(err) => {
                failures += 1;
                let error = BenchmarkCaseError::Distributed(err.map(StringifiedError::from_err));
                (reporter.report_error(&args, &error), Err(error))
            },
        };

        results.insert(
            args.get_id(),
            BenchmarkCaseReport {
                dataset: Cow::Borrowed(args.dataset.path()),
                format: args.dataset.format(),
                variable: args.variable.summary(),
                compressor: args.compressor.summary(),
                result,
            },
        );

        if control.is_break() {
            break;
        }
    }

    // Consume the remaining cases to ensure that num_cases is correct
    cases.for_each(|_| ());

    BenchmarkReport {
        settings: settings_clone,
        results,
        summary: BenchmarkSummary {
            success,
            failures,
            cancelled: num_cases - (success + failures),
        },
    }
}
