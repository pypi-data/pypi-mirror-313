use thiserror::Error;

use core_error::LocationError;

use crate::Reaper;

#[derive(Debug, Error)]
#[error("failed to wait for the forked child process")]
pub struct ChildWaitError;

pub enum Fork {
    Child(ForkChild),
    Parent(ForkParent),
}

pub struct ForkChild {
    _private: (),
}

pub struct ForkParent {
    child_pid: rustix::process::Pid,
    _private: (),
}

impl ForkParent {
    /// Wait for the forked child process to terminate.
    ///
    /// # Errors
    /// Returns the [`std::io::Error`] if waiting on the child process failed.
    pub fn wait_for_child(self) -> Result<(), LocationError<std::io::Error>> {
        loop {
            match rustix::process::waitpid(
                Some(self.child_pid),
                rustix::process::WaitOptions::NOHANG,
            ) {
                Err(err) => return Err(LocationError::from2(err)),
                Ok(None) => continue,
                Ok(Some(_)) => return Ok(()),
            }
        }
    }

    /// Try to wait for the forked child process to terminate. If the child has
    /// not yet terminated, [`Self`] is returned to try again.
    ///
    /// # Errors
    /// Returns the [`std::io::Error`] if waiting on the child process failed.
    pub fn try_wait_for_child(self) -> Result<Result<(), Self>, LocationError<std::io::Error>> {
        match rustix::process::waitpid(Some(self.child_pid), rustix::process::WaitOptions::NOHANG) {
            Err(err) => Err(LocationError::from2(err)),
            Ok(None) => Ok(Err(self)),
            Ok(Some(_)) => Ok(Ok(())),
        }
    }

    pub(crate) const fn child_pid(&self) -> rustix::process::Pid {
        self.child_pid
    }
}

impl Reaper {
    /// Forks the current process and returns on the child and the parent
    /// process. [`Fork`] indicates if the process is the child or parent
    /// on success.
    ///
    /// # Errors
    /// Returns the [`std::io::Error`] if forking child process failed.
    pub fn fork(&self) -> Result<Fork, LocationError<std::io::Error>> {
        // FIXME
        // see https://docs.rs/rustix/0.38.32/src/rustix/runtime.rs.html#232-317
        #[expect(unsafe_code)]
        let child_pid = unsafe { libc::fork() };

        match rustix::process::Pid::from_raw(child_pid) {
            None if child_pid == 0 => Ok(Fork::Child(ForkChild { _private: () })),
            None => Err(std::io::Error::last_os_error().into()),
            Some(child_pid) => Ok(Fork::Parent(ForkParent {
                child_pid,
                _private: (),
            })),
        }
    }
}
