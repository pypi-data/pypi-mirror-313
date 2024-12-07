use signal_hook::iterator::Signals;
use thiserror::Error;

use core_error::LocationError;

use super::{exit_with_report, worker::reaper_worker};
use crate::{Fork, Reaper};

pub fn reaper_handler_setup<F: FnOnce(&Reaper) -> Q, Q>(
    canary_pid: rustix::process::Pid,
    inner: F,
) -> Result<Q, LocationError<HandlerSetupError>> {
    let handler_pid = rustix::process::getpid();

    #[cfg(target_os = "linux")]
    if let Err(err) =
        rustix::process::set_parent_process_death_signal(Some(rustix::process::Signal::Child))
    {
        return Err(HandlerSetupError::DeathSignalSetup(err.into()).into());
    }
    if let Err(err) = rustix::process::setsid() {
        return Err(HandlerSetupError::ProcessGroupSetup(err.into()).into());
    }
    #[cfg(target_os = "linux")]
    if let Err(err) = rustix::process::set_child_subreaper(Some(handler_pid)) {
        return Err(HandlerSetupError::SubReaperSetup(err.into()).into());
    }

    // Check if the canary quit before the handler, if so abort
    if rustix::process::getppid() != Some(canary_pid) {
        log::warn!(
            "The CANARY {canary_pid:?} has been terminated before the HANDLER {handler_pid:?} \
             could start."
        );

        std::process::abort();
    }

    match Reaper::new().fork() {
        Err(err) => Err(HandlerSetupError::HandlerForkError(err).into()),
        Ok(Fork::Child(_)) => match reaper_worker(inner) {
            Ok(result) => Ok(result),
            Err(err) => exit_with_report(err),
        },
        Ok(Fork::Parent(parent)) => {
            match reaper_handler(canary_pid, handler_pid, parent.child_pid()) {
                Ok(status) => std::process::exit(status),
                Err(err) => exit_with_report(err),
            }
        },
    }
}

fn reaper_handler(
    canary_pid: rustix::process::Pid,
    handler_pid: rustix::process::Pid,
    worker_pid: rustix::process::Pid,
) -> Result<i32, LocationError<HandlerError>> {
    let mut signals =
        Signals::new((1..32).filter(|signal| !signal_hook::consts::FORBIDDEN.contains(signal)))
            .map_err(HandlerError::SignalInstallation)?;

    let status = 'outer: loop {
        match rustix::process::waitpid(Some(worker_pid), rustix::process::WaitOptions::NOHANG) {
            Err(err) => return Err(HandlerError::WorkerWait(err.into()).into()),
            Ok(None) => (),
            #[expect(clippy::cast_possible_wrap)] // FIXME
            Ok(Some(status)) => break libc::WEXITSTATUS(status.as_raw() as i32),
        };

        for signal in signals.wait() {
            let Some(signal) = rustix::process::Signal::from_raw(signal) else {
                return Err(HandlerError::UnknownSignal(signal).into());
            };

            log::debug!("The HANDLER {handler_pid:?} has received the signal {signal:?}.");

            if signal != rustix::process::Signal::Child {
                log::debug!(
                    "The HANDLER {handler_pid:?} will send the signal {signal:?} to the WORKER \
                     group {worker_pid:?}."
                );

                // Error is ignored as the worker may have already terminated
                let _ = rustix::process::kill_process_group(worker_pid, signal);
            } else if rustix::process::getppid() != Some(canary_pid) {
                log::debug!(
                    "The HANDLER {handler_pid:?} has been informed that the CANARY {canary_pid:?} \
                     has died."
                );
                log::debug!(
                    "The HANDLER {handler_pid:?} will terminate the WORKER group {worker_pid:?}."
                );

                // Error is ignored as the worker may have already terminated
                let _ =
                    rustix::process::kill_process_group(worker_pid, rustix::process::Signal::Kill);

                log::debug!(
                    "The HANDLER {handler_pid:?} will wait for the WORKER leader {worker_pid:?}."
                );

                match rustix::process::waitpid(
                    Some(worker_pid),
                    rustix::process::WaitOptions::empty(),
                ) {
                    Err(err) => return Err(HandlerError::WorkerWait(err.into()).into()),
                    Ok(None) => {
                        return Err(HandlerError::WorkerWait(std::io::Error::last_os_error()).into())
                    },
                    #[expect(clippy::cast_possible_wrap)] // FIXME
                    Ok(Some(status)) => break 'outer libc::WEXITSTATUS(status.as_raw() as i32),
                }
            }
        }
    };

    log::debug!("The HANDLER {handler_pid:?} will wait for the WORKER group {worker_pid:?}.");

    // Error means that we haved waited for all children
    while rustix::process::wait(rustix::process::WaitOptions::NOHANG).is_ok() {}

    log::debug!("The HANDLER {handler_pid:?} will exit with status {status}.");

    Ok(status)
}

#[derive(Debug, Error)]
pub enum HandlerSetupError {
    #[cfg(target_os = "linux")]
    #[error("failed to setup the death signal in the handler")]
    DeathSignalSetup(#[source] std::io::Error),
    #[error("failed to create a new process group for the handler")]
    ProcessGroupSetup(#[source] std::io::Error),
    #[cfg(target_os = "linux")]
    #[error("failed to make the handler a sub-reaper for its descendants")]
    SubReaperSetup(#[source] std::io::Error),
    #[error("failed to fork the handler process into a handler and a worker")]
    HandlerForkError(#[source] LocationError<std::io::Error>),
}

#[derive(Debug, Error)]
enum HandlerError {
    #[error("failed to install the signal handler in the handler")]
    SignalInstallation(#[source] std::io::Error),
    #[error("failed to wait for the worker to terminate")]
    WorkerWait(#[source] std::io::Error),
    #[error("failed to forward unknown signal {0} to the worker group")]
    UnknownSignal(i32),
}
