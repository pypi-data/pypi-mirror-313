use std::{
    borrow::Cow,
    fs::{self, File},
    io::{self, Write},
    ops::ControlFlow,
    path::Path,
};

use nonempty::NonEmpty;
use vecmap::VecSet;

use core_benchmark::{
    case::{BenchmarkCase, BenchmarkCaseId},
    measuring::{CodecBenchmarkStats, CompressorBenchmarkStats, GoodnessBenchmarkStats},
    report::{BenchmarkCaseOutput, BenchmarkReport},
    reporter::BenchmarkReporter,
};
use core_dataset::variable::derivative::DataDerivative;
use core_error::LocationError;

use super::{BenchmarkCaseError, BenchmarkCaseReport, BenchmarkSettings, BenchmarkSummary};

pub struct ProgressReporter {
    success: usize,
    failure: usize,
}

impl ProgressReporter {
    #[must_use]
    pub const fn new() -> Self {
        Self {
            success: 0,
            failure: 0,
        }
    }

    fn report_case(&self, summary: &'static str, case: &BenchmarkCase) {
        println!(
            "  - [{}]: {summary} ({} ok, {} err)",
            self.success + self.failure,
            self.success,
            self.failure
        );
        println!("    - case: {}", case.get_uuid());
        println!("    - compressor: {}", case.compressor);
        println!("    - variable: {}", case.variable.name());
        println!("    - dataset: {:?}", case.dataset.path());
    }
}

impl BenchmarkReporter for ProgressReporter {
    fn report_success(
        &mut self,
        case: &BenchmarkCase,
        _result: &BenchmarkCaseOutput,
    ) -> ControlFlow<()> {
        self.success += 1;

        self.report_case("SUCCESS", case);

        ControlFlow::Continue(())
    }

    fn report_error(
        &mut self,
        case: &BenchmarkCase,
        _error: &BenchmarkCaseError,
    ) -> ControlFlow<()> {
        self.failure += 1;

        self.report_case("ERROR", case);

        ControlFlow::Continue(())
    }
}

pub struct MinimalErrorReporter;

impl BenchmarkReporter for MinimalErrorReporter {
    fn report_error(
        &mut self,
        _case: &BenchmarkCase,
        error: &BenchmarkCaseError,
    ) -> ControlFlow<()> {
        println!("    - error: {:#}", anyhow::Error::new(error.clone()));
        ControlFlow::Continue(())
    }
}

pub struct VerboseConsoleReporter;

impl BenchmarkReporter for VerboseConsoleReporter {
    #[expect(clippy::too_many_lines)]
    fn report_success(
        &mut self,
        BenchmarkCase {
            dataset: _,
            variable,
            compressor,
        }: &BenchmarkCase,
        BenchmarkCaseOutput {
            stats:
                CompressorBenchmarkStats {
                    goodness:
                        NonEmpty {
                            head: baseline_goodness,
                            tail: derivatives_goodness,
                        },
                    throughput,
                    instructions,
                    compression_ratio,
                    per_codec,
                },
        }: &BenchmarkCaseOutput,
    ) -> ControlFlow<()> {
        println!("    - goodness:");
        println!("      - {}:", variable.name());
        println!("        - uniformity: {:10}", baseline_goodness.uniformity);
        println!(
            "        - uniformity (rel): {:10}",
            baseline_goodness.uniformity_rel
        );
        println!(
            "        - correlation (abs): {:10}",
            baseline_goodness.correlation
        );
        println!(
            "        - preserved PCA: {:10}",
            baseline_goodness.preserved_pca
        );
        println!(
            "        - bit information ratio: {:10}",
            baseline_goodness.bit_information
        );
        println!("        - error: {:10}", baseline_goodness.error);
        println!("        - error (abs): {:10}", baseline_goodness.error_abs);
        println!("        - error (rel): {:10}", baseline_goodness.error_rel);
        println!(
            "        - error (abs(rel)): {:10}",
            baseline_goodness.error_rel_abs
        );
        println!(
            "        - error (RMSE): {:10}",
            baseline_goodness.error_rmse
        );
        println!(
            "        - peak signal-to-noise ratio: {:10}",
            baseline_goodness.ps2nr
        );

        for (
            derivatives,
            GoodnessBenchmarkStats {
                uniformity,
                uniformity_rel,
                correlation,
                preserved_pca,
                bit_information,
                error,
                error_abs,
                error_rel,
                error_rel_abs,
                error_rmse,
                ps2nr,
            },
        ) in variable
            .derivatives()
            .iter()
            .zip(derivatives_goodness.iter())
        {
            print!("      - {}", variable.name());
            for derivative in derivatives {
                match derivative {
                    DataDerivative::Differentiate { differentiate } => {
                        print!(" ∂ {differentiate}");
                    },
                    DataDerivative::Integrate { integrate } => print!(" ∫ {integrate}"),
                }
            }
            println!(":");
            println!("        - uniformity: {uniformity:10}");
            println!("        - uniformity (rel): {uniformity_rel:10}");
            println!("        - correlation (abs): {correlation:10}");
            println!("        - preserved PCA: {preserved_pca:10}");
            println!("        - bit information ratio: {bit_information:10}");
            println!("        - error: {error:10}");
            println!("        - error (abs): {error_abs:10}");
            println!("        - error (rel): {error_rel:10}");
            println!("        - error (abs(rel)): {error_rel_abs:10}");
            println!("        - error (RMSE): {error_rmse:10}");
            println!("        - peak signal-to-noise ratio: {ps2nr:10}");
        }

        println!("    - total throughput: {throughput:6}");
        if let Some(instructions) = instructions {
            println!("    - total instructions: {instructions:6}");
        }
        println!("    - compression ratio: {compression_ratio:6}");
        println!("    - per-codec encode/decode:");

        for (
            codec,
            CodecBenchmarkStats {
                compression_ratio,
                encode_throughput,
                decode_throughput,
                encode_instructions,
                decode_instructions,
                encoded_bytes,
                decoded_bytes,
            },
        ) in compressor.codecs().zip(per_codec.iter())
        {
            println!("      - {codec}:");
            println!("        - compression ratio: {compression_ratio:10}");
            println!("        - encode throughput: {encode_throughput:10}");
            println!("        - decode throughput: {decode_throughput:10}");
            if let Some(encode_instructions) = encode_instructions {
                println!("        - encode instructions: {encode_instructions:10}");
            }
            if let Some(decode_instructions) = decode_instructions {
                println!("        - decode instructions: {decode_instructions:10}");
            }
            println!("        - encoded bytes: {encoded_bytes:10}");
            println!("        - decoded bytes: {decoded_bytes:10}");
        }

        ControlFlow::Continue(())
    }

    fn report_error(
        &mut self,
        _args: &BenchmarkCase,
        error: &BenchmarkCaseError,
    ) -> ControlFlow<()> {
        println!("    - error: {:#}", anyhow::Error::new(error.clone()));

        ControlFlow::Continue(())
    }
}

pub struct ErrorLogReporter;

impl BenchmarkReporter for ErrorLogReporter {
    fn report_error(
        &mut self,
        _args: &BenchmarkCase,
        error: &BenchmarkCaseError,
    ) -> ControlFlow<()> {
        log::error!(
            "single benchmark error: {:#}",
            anyhow::Error::new(error.clone())
        );
        ControlFlow::Continue(())
    }
}

pub struct JsonReporter {
    file: File,
    error: Option<LocationError<io::Error>>,
    first: bool,
    pre_success: usize,
    pre_failures: usize,
}

impl JsonReporter {
    pub fn create(
        path: &Path,
        settings: &BenchmarkSettings,
    ) -> Result<Self, LocationError<io::Error>> {
        let mut file = File::options().create_new(true).write(true).open(path)?;

        write!(file, "{{\"settings\":")?;
        serde_json::to_writer(&mut file, settings).map_err(io::Error::from)?;
        write!(file, ",\"results\":{{")?;

        Ok(Self {
            file,
            error: None,
            first: true,
            pre_success: 0,
            pre_failures: 0,
        })
    }

    pub fn resume(
        path: &Path,
        settings: &BenchmarkSettings,
    ) -> Result<(Self, VecSet<BenchmarkCaseId>), LocationError<io::Error>> {
        let mut json_report = fs::read(path)?;

        // Read in the existing report without re-validating every part
        let partial_report: BenchmarkReport = match serde_json::from_slice(&json_report) {
            Ok(partial_report) => Ok(partial_report),
            Err(err) => {
                // Try again with closing brackets in case the benchmark
                //  terminated unexpectedly
                json_report.push(b'}');
                json_report.push(b',');
                serde_json::to_writer(&mut json_report, &BenchmarkSummary::default())
                    .map_err(io::Error::from)?;
                json_report.push(b'}');
                serde_json::from_slice(&json_report).map_err(|_| io::Error::from(err))
            },
        }?;

        // NOTE: since arguments are already resolved at this point,
        //        they need to be passed explicitly
        if settings != &partial_report.settings {
            return Err(io::Error::new(
                io::ErrorKind::InvalidInput,
                format!(
                    "resume settings {:#?} do not match current settings {settings:#?}",
                    partial_report.settings
                ),
            )
            .into());
        }

        let mut pre_success = 0;
        let mut pre_failures = 0;

        // Collect the IDs of all already completed cases and bootstrap the summary
        let completed_cases: VecSet<BenchmarkCaseId> = partial_report
            .results
            .iter()
            .filter_map(|(id, result)| {
                match result.result {
                    Ok(_) => {
                        pre_success += 1;
                        Some(*id)
                    },
                    // We give distributed failures another chance
                    Err(BenchmarkCaseError::Distributed { .. }) => None,
                    // We give keyboard interrupt failures another chance
                    Err(BenchmarkCaseError::Python(ref err))
                        if err.error().message().starts_with("KeyboardInterrupt:") =>
                    {
                        None
                    },
                    Err(_) => {
                        pre_failures += 1;
                        Some(*id)
                    },
                }
            })
            .collect();

        // Overwrite the existing report file so that we can continue appending
        //  no matter where the last benchmark left off
        let mut file = File::options().truncate(true).write(true).open(path)?;

        write!(file, "{{\"settings\":")?;
        serde_json::to_writer(&mut file, settings).map_err(io::Error::from)?;
        write!(file, ",\"results\":{{")?;

        let mut completed_cases_iter = completed_cases.iter().peekable();

        // Replay all existing results into the JSON report
        let mut first = true;
        for (id, result) in partial_report.results {
            // Ensure that we only write out accepted completed cases
            match completed_cases_iter.peek() {
                Some(next_id) if id == **next_id => {
                    let _ = completed_cases_iter.next();
                },
                Some(_) => continue,
                None => break,
            }

            if !first {
                write!(file, ",")?;
            }
            first = false;

            serde_json::to_writer(&mut file, &id).map_err(io::Error::from)?;
            write!(file, ":")?;
            serde_json::to_writer(&mut file, &result).map_err(io::Error::from)?;
        }

        file.flush()?;

        Ok((
            Self {
                file,
                error: None,
                first,
                pre_success,
                pre_failures,
            },
            completed_cases,
        ))
    }

    pub fn report_case(
        &mut self,
        args: &BenchmarkCase,
        result: Result<&BenchmarkCaseOutput, &BenchmarkCaseError>,
    ) -> Result<(), LocationError<io::Error>> {
        if let Some(err) = self.error.take() {
            return Err(err);
        }

        if !self.first {
            write!(self.file, ",")?;
        }
        self.first = false;

        serde_json::to_writer(&mut self.file, &args.get_id()).map_err(io::Error::from)?;
        write!(self.file, ":")?;
        serde_json::to_writer(
            &mut self.file,
            &BenchmarkCaseReport {
                dataset: Cow::Borrowed(args.dataset.path()),
                format: args.dataset.format(),
                variable: args.variable.summary(),
                compressor: args.compressor.summary(),
                result: match result {
                    Ok(ok) => Ok(ok.clone()),
                    Err(err) => Err(err.clone()),
                },
            },
        )
        .map_err(io::Error::from)?;

        self.file.flush()?;

        Ok(())
    }

    pub fn finalise(mut self, summary: &BenchmarkSummary) -> Result<(), LocationError<io::Error>> {
        self.first = false;

        if let Some(err) = self.error.take() {
            return Err(err);
        }

        let complete_summary = BenchmarkSummary {
            success: summary.success + self.pre_success,
            failures: summary.failures + self.pre_failures,
            cancelled: summary.cancelled,
        };

        write!(self.file, "}},\"summary\":")?;
        serde_json::to_writer(&mut self.file, &complete_summary).map_err(io::Error::from)?;
        write!(self.file, "}}")?;

        self.file.flush()?;

        Ok(())
    }
}

impl Drop for JsonReporter {
    fn drop(&mut self) {
        if self.error.take().is_none() && self.first {
            std::mem::drop(write!(self.file, "}}}}"));
            std::mem::drop(self.file.flush());
        }
    }
}

impl BenchmarkReporter for JsonReporter {
    fn report_success(
        &mut self,
        args: &BenchmarkCase,
        result: &BenchmarkCaseOutput,
    ) -> ControlFlow<()> {
        match self.report_case(args, Ok(result)) {
            Ok(()) => ControlFlow::Continue(()),
            Err(err) => {
                self.error = Some(err);
                ControlFlow::Break(())
            },
        }
    }

    fn report_error(
        &mut self,
        args: &BenchmarkCase,
        error: &BenchmarkCaseError,
    ) -> ControlFlow<()> {
        match self.report_case(args, Err(error)) {
            Ok(()) => ControlFlow::Continue(()),
            Err(err) => {
                self.error = Some(err);
                ControlFlow::Break(())
            },
        }
    }
}
