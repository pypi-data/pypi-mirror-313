use std::ops::ControlFlow;

use crate::{error::BenchmarkCaseError, report::BenchmarkCaseOutput, BenchmarkCase};

pub trait BenchmarkReporter {
    fn report_success(
        &mut self,
        args: &BenchmarkCase,
        result: &BenchmarkCaseOutput,
    ) -> ControlFlow<()> {
        let _ = (args, result);
        ControlFlow::Continue(())
    }

    fn report_error(
        &mut self,
        args: &BenchmarkCase,
        error: &BenchmarkCaseError,
    ) -> ControlFlow<()> {
        let _ = (args, error);
        ControlFlow::Continue(())
    }
}

impl<R: ?Sized + BenchmarkReporter> BenchmarkReporter for Box<R> {
    fn report_success(
        &mut self,
        args: &BenchmarkCase,
        result: &BenchmarkCaseOutput,
    ) -> ControlFlow<()> {
        (**self).report_success(args, result)
    }

    fn report_error(
        &mut self,
        args: &BenchmarkCase,
        error: &BenchmarkCaseError,
    ) -> ControlFlow<()> {
        (**self).report_error(args, error)
    }
}

impl<R: ?Sized + BenchmarkReporter> BenchmarkReporter for &mut R {
    fn report_success(
        &mut self,
        args: &BenchmarkCase,
        result: &BenchmarkCaseOutput,
    ) -> ControlFlow<()> {
        (*self).report_success(args, result)
    }

    fn report_error(
        &mut self,
        args: &BenchmarkCase,
        error: &BenchmarkCaseError,
    ) -> ControlFlow<()> {
        (*self).report_error(args, error)
    }
}

fn report_all_success(
    it: impl Iterator<Item = impl BenchmarkReporter>,
    args: &BenchmarkCase,
    result: &BenchmarkCaseOutput,
) -> ControlFlow<()> {
    // forward successful result to all reporters without short circuiting
    #[expect(clippy::manual_try_fold)]
    it.fold(ControlFlow::Continue(()), |control, mut reporter| {
        match (reporter.report_success(args, result), control) {
            (ControlFlow::Continue(()), ControlFlow::Continue(())) => ControlFlow::Continue(()),
            _ => ControlFlow::Break(()),
        }
    })
}

fn report_all_error(
    it: impl Iterator<Item = impl BenchmarkReporter>,
    args: &BenchmarkCase,
    error: &BenchmarkCaseError,
) -> ControlFlow<()> {
    // forward error to all reporters without short circuiting
    #[expect(clippy::manual_try_fold)]
    it.fold(ControlFlow::Continue(()), |control, mut reporter| {
        match (reporter.report_error(args, error), control) {
            (ControlFlow::Continue(()), ControlFlow::Continue(())) => ControlFlow::Continue(()),
            _ => ControlFlow::Break(()),
        }
    })
}

impl<'a> BenchmarkReporter for &'a mut [&'a mut dyn BenchmarkReporter] {
    fn report_success(
        &mut self,
        args: &BenchmarkCase,
        result: &BenchmarkCaseOutput,
    ) -> ControlFlow<()> {
        report_all_success(self.iter_mut(), args, result)
    }

    fn report_error(
        &mut self,
        args: &BenchmarkCase,
        error: &BenchmarkCaseError,
    ) -> ControlFlow<()> {
        report_all_error(self.iter_mut(), args, error)
    }
}

impl BenchmarkReporter for &mut [Box<dyn BenchmarkReporter>] {
    fn report_success(
        &mut self,
        args: &BenchmarkCase,
        result: &BenchmarkCaseOutput,
    ) -> ControlFlow<()> {
        report_all_success(self.iter_mut(), args, result)
    }

    fn report_error(
        &mut self,
        args: &BenchmarkCase,
        error: &BenchmarkCaseError,
    ) -> ControlFlow<()> {
        report_all_error(self.iter_mut(), args, error)
    }
}

pub struct StopForError;

impl BenchmarkReporter for StopForError {
    fn report_error(
        &mut self,
        _args: &BenchmarkCase,
        _error: &BenchmarkCaseError,
    ) -> ControlFlow<()> {
        ControlFlow::Break(())
    }
}
