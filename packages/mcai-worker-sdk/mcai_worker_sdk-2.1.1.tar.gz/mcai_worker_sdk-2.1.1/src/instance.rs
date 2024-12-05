#[cfg(feature = "media")]
use crate::media;
#[cfg(not(feature = "media"))]
use crate::{
  callback::CallbackHandle, helper::get_destination_paths, helper::get_parameters,
  WORKER_METHOD_PROCESS,
};
use crate::{description::WorkerDescription, parameters::WorkerParameters, WORKER_METHOD_INIT};

use mcai_worker_sdk::prelude::*;
use pyo3::{prelude::*, types::PyType};
use schemars::schema::RootSchema;

#[cfg(feature = "media")]
use pyo3::types::PyList;
#[cfg(feature = "media")]
use std::{
  convert::TryInto,
  ops::Deref,
  sync::{mpsc::Sender, Arc, Mutex},
};

pub struct WorkerInstance {
  worker: Py<PyAny>,
  parameters: Py<PyType>,
  description: WorkerDescription,
  #[cfg(feature = "media")]
  result: Option<Arc<Mutex<Sender<ProcessResult>>>>,
}

impl WorkerInstance {
  pub fn new(worker: Py<PyAny>, parameters: Py<PyType>, description: WorkerDescription) -> Self {
    Self {
      worker,
      parameters,
      description,
      #[cfg(feature = "media")]
      result: None,
    }
  }
}

impl McaiWorker<WorkerParameters, WorkerDescription> for WorkerInstance {
  fn get_parameters_schema(&self) -> Result<RootSchema> {
    WorkerParameters::get_schema(&self.parameters)
      .map_err(|err| MessageError::RuntimeError(err.to_string()))
  }

  fn get_mcai_worker_description(&self) -> Box<WorkerDescription> {
    Box::new(self.description.clone())
  }

  fn init(&mut self) -> Result<()> {
    Python::with_gil(|py| -> PyResult<PyObject> {
      self.worker.call_method0(py, WORKER_METHOD_INIT)
    })
    .map_err(|err| MessageError::RuntimeError(err.to_string()))?;
    Ok(())
  }

  #[cfg(feature = "media")]
  fn init_process(
    &mut self,
    parameters: WorkerParameters,
    format_context: Arc<Mutex<FormatContext>>,
    result: Arc<Mutex<Sender<ProcessResult>>>,
  ) -> Result<Vec<StreamDescriptor>> {
    self.result = Some(result);

    parameters.validate_parameters(&self.parameters)?;

    let context = media::FormatContext::from(format_context);
    let stream_descriptors = Python::with_gil(|py| -> PyResult<Vec<StreamDescriptor>> {
      let worker_parameters = self.parameters.to_object(py);
      parameters.to_python_parameters(&worker_parameters)?;

      let stream_descriptors = self.worker.call_method1(
        py,
        media::WORKER_METHOD_INIT_PROCESS,
        (context, worker_parameters),
      )?;

      media::get_stream_descriptors(stream_descriptors.downcast_bound::<PyList>(py)?)
    })
    .map_err(|error_message| MessageError::RuntimeError(error_message.to_string()))?;

    Ok(stream_descriptors)
  }

  #[cfg(feature = "media")]
  fn process_frames(
    &mut self,
    job_result: JobResult,
    stream_index: usize,
    process_frames: &[ProcessFrame],
  ) -> Result<ProcessResult> {
    let mut media_frames: Vec<media::Frame> = vec![];
    let mut ebu_ttml_frames: Vec<media::PyEbuTtmlLive> = vec![];

    if process_frames.is_empty() {
      return Ok(ProcessResult::empty());
    }

    for process_frame in process_frames {
      match &process_frame {
        ProcessFrame::AudioVideo(frame) => {
          media_frames.push(frame.try_into()?);
        }
        ProcessFrame::EbuTtmlLive(ebu_ttml_live) => {
          ebu_ttml_frames.push(ebu_ttml_live.deref().clone().into());
        }
        ProcessFrame::Json(_)
        | ProcessFrame::Data(_)
        | ProcessFrame::WebVtt(_)
        | ProcessFrame::SubRip(_) => {}
      }
    }

    if !media_frames.is_empty() {
      let response = Python::with_gil(|py| -> PyResult<PyObject> {
        self.worker.call_method1(
          py,
          media::WORKER_METHOD_PROCESS_FRAMES,
          (&job_result.get_str_job_id(), stream_index, media_frames),
        )
      })
      .map_err(|error_message| {
        let result = job_result
          .with_status(JobStatus::Error)
          .with_message(&error_message.to_string());
        MessageError::ProcessingError(result)
      })?;

      Ok(ProcessResult::new_json(response.to_string()))
    } else if !ebu_ttml_frames.is_empty() {
      let response = Python::with_gil(|py| -> PyResult<PyObject> {
        self.worker.call_method1(
          py,
          media::WORKER_METHOD_PROCESS_EBU_TTML_LIVE,
          (&job_result.get_str_job_id(), stream_index, ebu_ttml_frames),
        )
      })
      .map_err(|error_message| {
        let result = job_result
          .with_status(JobStatus::Error)
          .with_message(&error_message.to_string());
        MessageError::ProcessingError(result)
      })?;

      Ok(ProcessResult::new_json(response.to_string()))
    } else {
      Err(MessageError::NotImplemented())
    }
  }

  #[cfg(feature = "media")]
  fn ending_process(&mut self) -> Result<()> {
    Python::with_gil(|py| -> PyResult<PyObject> {
      self
        .worker
        .call_method0(py, media::WORKER_METHOD_ENDING_PROCESS)
    })
    .map_err(|error_message| MessageError::RuntimeError(error_message.to_string()))?;

    if let Some(result) = &self.result {
      result
        .lock()
        .unwrap()
        .send(ProcessResult::end_of_process())
        .unwrap();
    }

    Ok(())
  }

  #[cfg(not(feature = "media"))]
  fn process(
    &self,
    channel: Option<McaiChannel>,
    parameters: WorkerParameters,
    mut job_result: JobResult,
  ) -> Result<JobResult> {
    parameters.validate_parameters(&self.parameters)?;

    let job_status = Arc::new(Mutex::new(None));
    let message = Arc::new(Mutex::new(None));

    let callback_handle = CallbackHandle {
      channel,
      job_id: job_result.get_job_id(),
      job_status: job_status.clone(),
      message: message.clone(),
    };

    let job_result_cloned = job_result.clone();

    job_result = Python::with_gil(|py| -> PyResult<JobResult> {
      let worker_parameters = self.parameters.to_object(py);
      parameters.to_python_parameters(&worker_parameters)?;

      let response = self.worker.call_method1(
        py,
        WORKER_METHOD_PROCESS,
        (callback_handle, worker_parameters, job_result.get_job_id()),
      )?;

      if let Some(mut destination_paths) = get_destination_paths(response.bind(py)) {
        job_result = job_result.with_destination_paths(&mut destination_paths);
      }

      if let Some(mut parameters) = get_parameters(response.bind(py)) {
        job_result = job_result.with_parameters(&mut parameters);
      }

      Ok(job_result)
    })
    .map_err(|error_message| {
      let result = job_result_cloned
        .with_status(JobStatus::Error)
        .with_message(&error_message.to_string());
      MessageError::ProcessingError(result)
    })?;

    // If no status has been set, default to Completed
    let final_status = job_status
      .lock()
      .unwrap()
      .as_ref()
      .unwrap_or(&JobStatus::Completed)
      .clone();

    match final_status {
      JobStatus::Error => {
        let error_message = message
          .lock()
          .unwrap()
          .as_ref()
          .unwrap_or(&"No message for this error in worker".to_string())
          .clone();
        Err(MessageError::ProcessingError(
          job_result
            .clone()
            .with_status(final_status)
            .with_message(&error_message),
        ))
      }
      _ => Ok(job_result.with_status(final_status)),
    }
  }
}
