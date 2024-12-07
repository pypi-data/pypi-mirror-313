use thiserror::Error;

use core_error::LocationError;

use crate::Reaper;

pub fn reaper_worker<F: FnOnce(&Reaper) -> Q, Q>(
    inner: F,
) -> Result<Q, LocationError<WorkerSetupError>> {
    let worker_pid = rustix::process::getpid();

    if let Err(err) = rustix::process::setsid() {
        return Err(WorkerSetupError::ProcessGroupSetup(err.into()).into());
    }

    log::debug!("The WORKER {worker_pid:?} will now start to execute.");

    let result = inner(&Reaper::new());

    log::debug!("The WORKER {worker_pid:?} has finished executing.");

    Ok(result)
}

#[derive(Debug, Error)]
pub enum WorkerSetupError {
    #[error("failed to create a new process group for the worker")]
    ProcessGroupSetup(#[source] std::io::Error),
}
