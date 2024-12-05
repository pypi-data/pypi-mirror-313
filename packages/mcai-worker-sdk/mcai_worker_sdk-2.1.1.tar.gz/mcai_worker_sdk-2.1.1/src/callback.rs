use mcai_worker_sdk::prelude::*;
use pyo3::prelude::*;
use std::sync::{Arc, Mutex};

/// Enum representing the job status.
///
/// This enum is essentially to be used as :func:`~mcai_worker_sdk.McaiChannel.set_job_status` argument.
#[pyclass(eq, eq_int, name = "JobStatus")]
#[derive(Clone, PartialEq)]
pub enum PythonJobStatus {
  Completed,
  Stopped,
  Error,
}
/// Channel object that allows sending information (status, progression) about the job to the backend.
#[pyclass(name = "McaiChannel")]
pub struct CallbackHandle {
  pub channel: Option<McaiChannel>,
  pub job_id: u64,
  pub job_status: Arc<Mutex<Option<JobStatus>>>,
  pub message: Arc<Mutex<Option<String>>>,
}

#[pymethods]
impl CallbackHandle {
  /// Method for publishing the progression of the job.
  ///
  /// Arguments:
  ///   progression (int): progression of the job in percent.
  ///
  /// Returns:
  ///   bool: True if the publication of the progression was successfull, else False.
  fn publish_job_progression(&self, value: u8) -> bool {
    publish_job_progression(self.channel.clone(), self.job_id, value).is_ok()
  }

  /// Method for checking wether the current job is stopped.
  ///
  /// Returns:
  ///   bool: True if the current job is stopped, else False.
  fn is_stopped(&self) -> bool {
    if let Some(channel) = &self.channel {
      channel.lock().unwrap().is_stopped()
    } else {
      false
    }
  }

  /// Method for setting the job status to return to the backend.
  ///
  /// Arguments:
  ///   status (:class:`~mcai_worker_sdk.JobStatus`): status of the job.
  ///
  /// Returns:
  ///   bool: True if the status has been set properly, else False.
  fn set_job_status(&mut self, status: PythonJobStatus) -> bool {
    let mut job_status = self.job_status.lock().unwrap();
    *job_status = match status {
      PythonJobStatus::Completed => Some(JobStatus::Completed),
      PythonJobStatus::Stopped => Some(JobStatus::Stopped),
      PythonJobStatus::Error => Some(JobStatus::Error),
    };
    job_status.is_some()
  }

  /// Method for setting the error message to return to the backend.
  ///
  /// Arguments:
  ///   status (:class:`~String`): error message.
  ///
  /// Returns:
  ///   bool: True if the message has been set properly, else False.
  fn set_error_message(&mut self, error_message: String) -> bool {
    let mut message = self.message.lock().unwrap();
    *message = Some(error_message);
    message.is_some()
  }
}
