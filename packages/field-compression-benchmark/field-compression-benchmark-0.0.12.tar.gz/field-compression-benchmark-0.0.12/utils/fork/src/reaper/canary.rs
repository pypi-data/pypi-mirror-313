use signal_hook::iterator::Signals;
use thiserror::Error;

use core_error::LocationError;

use super::{exit_with_report, handler::reaper_handler_setup};
use crate::{Fork, Reaper};

pub fn reaper_canary_setup<F: FnOnce(&Reaper) -> Q, Q>(
    inner: F,
) -> Result<Q, LocationError<CanarySetupError>> {
    let canary_pid = rustix::process::getpid();

    match Reaper::new().fork() {
        Err(err) => Err(CanarySetupError::CanaryForkError(err).into()),
        Ok(Fork::Child(_)) => match reaper_handler_setup(canary_pid, inner) {
            Ok(result) => Ok(result),
            Err(err) => exit_with_report(err),
        },
        Ok(Fork::Parent(parent)) => match reaper_canary(canary_pid, parent.child_pid()) {
            Ok(status) => std::process::exit(status),
            Err(err) => exit_with_report(err),
        },
    }
}

fn reaper_canary(
    canary_pid: rustix::process::Pid,
    handler_pid: rustix::process::Pid,
) -> Result<i32, LocationError<CanaryError>> {
    let mut signals =
        Signals::new((1..32).filter(|signal| !signal_hook::consts::FORBIDDEN.contains(signal)))
            .map_err(CanaryError::SignalInstallation)?;

    let status = loop {
        match rustix::process::waitpid(Some(handler_pid), rustix::process::WaitOptions::NOHANG) {
            Err(err) => return Err(CanaryError::HandlerWait(err.into()).into()),
            Ok(None) => (),
            #[expect(clippy::cast_possible_wrap)] // FIXME
            Ok(Some(status)) => break libc::WEXITSTATUS(status.as_raw() as i32),
        };

        for signal in signals.wait() {
            let Some(signal) = rustix::process::Signal::from_raw(signal) else {
                return Err(CanaryError::UnknownSignal(signal).into());
            };

            log::debug!("The CANARY {canary_pid:?} has received the signal {signal:?}.");

            if signal != rustix::process::Signal::Child {
                log::debug!(
                    "The CANARY {handler_pid:?} will send the signal {signal:?} to the HANDLER \
                     {handler_pid:?}."
                );

                // Error is ignored as the handler may have already terminated
                let _ = rustix::process::kill_process(handler_pid, signal);
            }
        }
    };

    log::debug!("The CANARY {canary_pid:?} will exit with status {status}.");

    Ok(status)
}

#[derive(Debug, Error)]
pub enum CanarySetupError {
    #[error("failed to fork the main process into a canary and a handler")]
    CanaryForkError(#[source] LocationError<std::io::Error>),
}

#[derive(Debug, Error)]
enum CanaryError {
    #[error("failed to install the signal handler in the canary")]
    SignalInstallation(#[source] std::io::Error),
    #[error("failed to wait for the handler to terminate")]
    HandlerWait(#[source] std::io::Error),
    #[error("failed to forward unknown signal {0} to the handler")]
    UnknownSignal(i32),
}
