use std::{convert::Infallible, process::Termination, sync::Mutex};

use core_error::LocationError;

mod canary;
mod handler;
mod worker;

use canary::reaper_canary_setup;

pub struct Reaper(());

impl Reaper {
    const fn new() -> Self {
        Self(())
    }

    /// Initialise the current (main) process to clean up any child processes
    /// it spawns. If setting up the reaper fails, the process is terminated.
    pub fn with_subprocess_reaper<F: FnOnce(&Self) -> Q, Q>(
        token: private::ReaperToken,
        inner: F,
    ) -> Q {
        #[expect(clippy::drop_non_drop)]
        std::mem::drop(token);

        match reaper_canary_setup(inner) {
            Ok(result) => result,
            Err(err) => exit_with_report(err),
        }
    }
}

pub static REAPER_TOKEN: Mutex<Option<private::ReaperToken>> =
    Mutex::new(Some(private::ReaperToken));

mod private {
    pub struct ReaperToken;
}

fn exit_with_report<E: std::error::Error>(err: LocationError<E>) -> ! {
    let _code = Result::<Infallible, _>::Err(err).report();
    // FIXME: code.exit_process();
    std::process::exit(1);
}
