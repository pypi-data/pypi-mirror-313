use std::{
    collections::VecDeque, convert::Infallible, iter::FusedIterator, num::NonZeroUsize,
    process::Termination, time::Duration,
};

use ipc_channel::ipc::{channel, IpcError, IpcOneShotServer, IpcReceiver, IpcSender, TryRecvError};
use serde::{de::DeserializeOwned, Serialize};
use thiserror::Error;

use core_error::LocationError;

use crate::{Fork, ForkParent, Reaper};

/// Distributes work across several parallel worker processes. The `worker`
/// closure is executed once for every input item from the `work` iterator, each
/// running on a separate process.
pub fn distribute_work<
    'a,
    F: 'static + Fn(A) -> Q,
    I: IntoIterator<Item = A, IntoIter: 'a + FusedIterator>,
    A: 'a,
    Q: 'a + Serialize + DeserializeOwned,
>(
    reaper: &'a Reaper,
    worker: F,
    work: I,
    max_processes: NonZeroUsize,
    ordered: bool,
) -> impl Iterator<Item = (A, Result<Q, LocationError<DistributedWorkError>>)> + 'a {
    let mut queue = ForkedWorkIterator {
        reaper,
        worker,
        work: work.into_iter(),
        queue: VecDeque::with_capacity(max_processes.get()),
        max_processes: max_processes.get(),
        graveyard: Vec::with_capacity(max_processes.get()),
        ordered,
    };
    queue.fill_up_with_work();
    queue
}

#[derive(Debug, Error)]
pub enum DistributedWorkError {
    #[error("failed to fork the process")]
    Fork(#[source] LocationError<std::io::Error>),
    #[error("failed to create a oneshot channel to the worker process")]
    OneShotCreate(#[source] std::io::Error),
    #[error("failed to connect to the oneshot channel on the worker process")]
    OneShotWorker(#[source] std::io::Error),
    #[error("failed to send via the oneshot channel")]
    OneShotSend(#[source] ipc_channel::Error),
    #[error("failed to receive via the oneshot channel")]
    OneShotReceive(#[source] ipc_channel::Error),
    #[error("failed to connect to the oneshot channel on the parent process")]
    OneShotParent(#[source] ipc_channel::Error),
    #[error("failed to create a channel between the parent and worker process")]
    CreateChannel(#[source] std::io::Error),
    #[error("failed to send the work result from the worker process")]
    SendResult(#[source] ipc_channel::Error),
    #[error("failed to receive the work result from the worker process")]
    ReceiveResult(#[source] IpcError),
}

struct ForkedWorkIterator<
    'a,
    F: 'static + Fn(A) -> Q,
    I: FusedIterator<Item = A>,
    A,
    Q: Serialize + DeserializeOwned,
> {
    reaper: &'a Reaper,
    worker: F,
    work: I,
    queue: VecDeque<WorkItem<A, Q>>,
    max_processes: usize,
    graveyard: Vec<ForkParent>,
    ordered: bool,
}

impl<F: 'static + Fn(A) -> Q, I: FusedIterator<Item = A>, A, Q: Serialize + DeserializeOwned> Drop
    for ForkedWorkIterator<'_, F, I, A, Q>
{
    fn drop(&mut self) {
        for fork in self.graveyard.drain(..) {
            if let Err(err) = fork.wait_for_child() {
                log::warn!("worker process could not be awaited: {err}");
            }
        }
    }
}

impl<F: 'static + Fn(A) -> Q, I: FusedIterator<Item = A>, A, Q: Serialize + DeserializeOwned>
    ForkedWorkIterator<'_, F, I, A, Q>
{
    fn fill_up_with_work(&mut self) {
        while self.max_processes > 0 {
            let Some(work) = self.work.next() else { return };

            let (oneshot_server, oneshot_server_name) = match IpcOneShotServer::new() {
                Ok(oneshot) => oneshot,
                Err(err) => {
                    self.queue.push_back(WorkItem::Done {
                        args: work,
                        result: Err(DistributedWorkError::OneShotCreate(err).into()),
                    });
                    // early return - perhaps the problem will be fixed the next time
                    return;
                },
            };

            match self.reaper.fork() {
                Err(err) => {
                    self.queue.push_back(WorkItem::Done {
                        args: work,
                        result: Err(DistributedWorkError::Fork(err).into()),
                    });
                    // early return - perhaps the problem will be fixed the next time
                    return;
                },
                Ok(Fork::Child(_)) => {
                    let oneshot_sender = match IpcSender::connect(oneshot_server_name) {
                        Ok(oneshot_sender) => oneshot_sender,
                        Err(err) => {
                            let _code = Result::<Infallible, _>::Err(
                                DistributedWorkError::OneShotWorker(err),
                            )
                            .report();
                            // FIXME: code.exit_process();
                            std::process::exit(1);
                        },
                    };
                    // the server should only be used in the parent process
                    std::mem::forget(oneshot_server);

                    let (result_sender, result_receiver) = match channel() {
                        Ok(oneshot_channel) => oneshot_channel,
                        Err(err) => {
                            let _code = Result::<Infallible, _>::Err(
                                DistributedWorkError::CreateChannel(err),
                            )
                            .report();
                            // FIXME: code.exit_process();
                            std::process::exit(1);
                        },
                    };
                    if let Err(err) = oneshot_sender.send(result_receiver) {
                        let _code =
                            Result::<Infallible, _>::Err(DistributedWorkError::OneShotSend(err))
                                .report();
                        // FIXME: code.exit_process();
                        std::process::exit(1);
                    };

                    match result_sender.send((self.worker)(work)) {
                        // FIXME: std::process::ExitCode::SUCCESS.exit_process();
                        Ok(()) => std::process::exit(0),
                        Err(err) => {
                            let _code =
                                Result::<Infallible, _>::Err(DistributedWorkError::SendResult(err))
                                    .report();
                            // FIXME: code.exit_process();
                            std::process::exit(1);
                        },
                    }
                },
                Ok(Fork::Parent(parent)) => {
                    let result_receiver = match oneshot_server.accept() {
                        Ok((_, result_receiver)) => result_receiver,
                        Err(err) => {
                            self.queue.push_back(WorkItem::Done {
                                args: work,
                                result: Err(DistributedWorkError::OneShotParent(err).into()),
                            });
                            // early return - perhaps the problem will be fixed the next time
                            return;
                        },
                    };

                    self.max_processes -= 1;

                    self.queue.push_back(WorkItem::InProgress {
                        args: work,
                        worker: parent,
                        receiver: result_receiver,
                    });
                },
            }
        }
    }

    fn clean_up_graveyard(&mut self) {
        let mut index = 0;

        while index < self.graveyard.len() {
            let fork = self.graveyard.swap_remove(index);

            match fork.try_wait_for_child() {
                Ok(Ok(())) => (),
                Ok(Err(fork)) => self.graveyard.push(fork),
                Err(err) => log::warn!("worker process could not be awaited: {err}"),
            }

            index += 1;
        }
    }
}

impl<F: 'static + Fn(A) -> Q, I: FusedIterator<Item = A>, A, Q: Serialize + DeserializeOwned>
    Iterator for ForkedWorkIterator<'_, F, I, A, Q>
{
    type Item = (A, Result<Q, LocationError<DistributedWorkError>>);

    fn next(&mut self) -> Option<Self::Item> {
        const DEFAULT_SLEEP: Duration = Duration::from_millis(8);
        const RESET_SLEEP: Duration = Duration::from_millis(1024);
        const MAX_SLEEP: Duration = Duration::from_millis(16384);

        let mut sleep_duration = DEFAULT_SLEEP;

        loop {
            // Try to start as many new worker processes as possible
            self.clean_up_graveyard();
            self.fill_up_with_work();

            let mut any_update = false;

            let mut index = 0;
            while let Some(item) = self.queue.swap_remove_back(index) {
                #[expect(clippy::never_loop)]
                // [ITEM] Compute the new version of the currently processed item
                let item = loop {
                    match item {
                        WorkItem::InProgress {
                            args,
                            worker,
                            receiver,
                        } => {
                            let result = match receiver.try_recv() {
                                Ok(result) => Ok(result),
                                // [ITEM] The in-progress item remains the same
                                Err(TryRecvError::Empty) => {
                                    break WorkItem::InProgress {
                                        args,
                                        worker,
                                        receiver,
                                    }
                                },
                                Err(TryRecvError::IpcError(err)) => {
                                    Err(DistributedWorkError::ReceiveResult(err).into())
                                },
                            };

                            any_update = true;

                            // Try to wait for the worker process to terminate
                            // Since we already have the result, non-critical wait errors
                            //  are only logged, not passed on further
                            match worker.try_wait_for_child() {
                                Ok(Ok(())) => (),
                                Ok(Err(worker)) => self.graveyard.push(worker),
                                Err(err) => {
                                    log::warn!("worker process could not be awaited: {err}");
                                },
                            };

                            self.max_processes += 1;

                            // [ITEM] The in-progress item is turned into a done item
                            break WorkItem::Done { args, result };
                        },
                        // [ITEM] The done item remains the same
                        WorkItem::Done { .. } => break item,
                    };
                };

                // Put the item back into the queue in the position from which it was removed
                self.queue.push_back(item);
                self.queue.swap(index, self.queue.len() - 1);

                index += 1;
            }

            if self.ordered {
                // Check whether the first work item in the queue is done, if so return it
                match self.queue.pop_front() {
                    None => return None,
                    Some(WorkItem::Done { args, result }) => return Some((args, result)),
                    Some(work) => self.queue.push_front(work),
                }
            } else if self.queue.is_empty() {
                return None;
            } else {
                // Check whether any work item in the queue is done, if so return it
                for _ in 0..self.queue.len() {
                    match self.queue.pop_front() {
                        None => return None,
                        Some(WorkItem::Done { args, result }) => return Some((args, result)),
                        Some(work) => self.queue.push_back(work),
                    }
                }
            }

            if any_update {
                if sleep_duration > RESET_SLEEP {
                    sleep_duration = RESET_SLEEP;
                } else {
                    sleep_duration /= 2;
                }
            } else if sleep_duration < MAX_SLEEP {
                sleep_duration *= 2;
            }

            log::trace!(
                "Sleeping for {sleep_duration:?} with queue={} graveyard={}",
                self.queue.len(),
                self.graveyard.len()
            );

            // If the first work item is not done yet, we wait
            std::thread::sleep(sleep_duration);
        }
    }

    fn size_hint(&self) -> (usize, Option<usize>) {
        let done = self.queue.len();

        match self.work.size_hint() {
            (lower, Some(upper)) => (lower + done, Some(upper + done)),
            (lower, None) => (lower + done, None),
        }
    }
}

// Correctness: ForkedWorkIterator is essentially a map over a fused iterator
impl<F: 'static + Fn(A) -> Q, I: FusedIterator<Item = A>, A, Q: Serialize + DeserializeOwned>
    FusedIterator for ForkedWorkIterator<'_, F, I, A, Q>
{
}

enum WorkItem<A, Q: Serialize + DeserializeOwned> {
    InProgress {
        args: A,
        worker: ForkParent,
        receiver: IpcReceiver<Q>,
    },
    Done {
        args: A,
        result: Result<Q, LocationError<DistributedWorkError>>,
    },
}
