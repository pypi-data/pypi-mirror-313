#[cfg(feature = "media")]
use crate::media;
use crate::{description::WorkerDescription, instance::WorkerInstance};

use mcai_worker_sdk::prelude::*;
use pyo3::{exceptions::PyNotImplementedError, prelude::*, types::PyType};

/// Worker base class to extend to define your own worker.
///
/// This class defines several abstract methods that may be re-implemented. However, most of them will be directly called and you won't need to call them explicitly.
///
/// Arguments:
///   parameters (:class:`~WorkerParameters`): Class definition of the worker's parameters.
///   description (:class:`~WorkerDescription`): Instance of WorkerDescription.
///
/// Warning:
///     The constructor may not be re-implemented. Use the :func:`~Worker.setup` method instead.
#[pyclass(subclass)]
#[derive(Clone, Debug)]
pub struct Worker {
  parameters: Option<Py<PyType>>, // This won't be exposed in Python
  description: Option<WorkerDescription>,
}

#[pymethods]
impl Worker {
  #[new]
  fn new(parameters: &Bound<'_, PyType>, description: WorkerDescription) -> Worker {
    Worker {
      parameters: Some(parameters.clone().unbind()),
      description: Some(description),
    }
  }

  fn __init__(
    &mut self,
    parameters: &Bound<'_, PyType>,
    description: WorkerDescription,
    _py: Python<'_>,
  ) -> PyResult<()> {
    self.parameters = Some(parameters.clone().unbind());
    self.description = Some(description);
    Ok(())
  }

  /// Method called once to set up the worker. This method should not be called explicitly but will be called automatically after worker initialization.
  ///
  /// This method may be used to load specific resources, perform checks, etc. before processing jobs.
  ///
  /// Note:
  ///   This method is optional but must be used instead of re-defining the constructor.
  fn setup(_self_: PyRef<'_, Self>) -> PyResult<()> {
    Ok(())
  }

  /// Method called for processing the job. This is were the major logic of your worker should reside.
  ///
  /// Arguments:
  ///   channel (:class:`~mcai_worker_sdk.McaiChannel`): Channel to send progression and status to MCAI backend.
  ///   parameters (:class:`~WorkerParameters`): Class definition of the worker's parameters.
  ///   job_id (int): ID of the current job.
  ///
  /// Returns:
  ///   dict: A dictionnary of key, values that will be sent back to MCAI backend.
  ///
  /// Raises:
  ///   NotImplementedError
  ///
  /// Note:
  ///   You do not have to call this method explicitly, but you must define it. It will be called everytime a job needs to be processed (*i.e* everytime a message arrives).
  #[cfg(not(feature = "media"))]
  fn process(_self_: PyRef<'_, Self>) -> PyResult<()> {
    Err(PyNotImplementedError::new_err(
      "Init process method must be implemented",
    ))
  }

  /// Method called for initializing the media process.
  ///
  /// It defines the streams that will be handled through :func:`~mcai_worker_sdk.Worker.process_frames` method and the FFmpeg filters that need to be applied.
  ///
  /// Arguments:
  ///   context (:class:`~mcai_worker_sdk.FormatContext`): Context describing the media to process.
  ///   parameters (:class:`~WorkerParameters`): Parameters received for the current job.
  ///
  /// Returns:
  ///   list: A list of :ref:`stream_descriptors` that will be handled during process
  ///
  /// Raises:
  ///   NotImplementedError
  #[cfg(feature = "media")]
  fn init_process(
    _self_: PyRef<'_, Self>,
    _format_context: Py<PyAny>,
    _parameters: Py<PyAny>,
  ) -> PyResult<Vec<media::GenericStreamDescriptor>> {
    Err(PyNotImplementedError::new_err(
      "Init process method must be implemented",
    ))
  }

  /// Method called for processing a batch of frames. This is were the major logic of your worker should reside.
  ///
  /// Arguments:
  ///   job_id (int): ID of the current job.
  ///   stream_index (int): Index of the current stream.
  ///   frames (list[:class:`~mcai_worker_sdk.Frame`]): The list of frames in the batch.
  ///
  /// Raises:
  ///   NotImplementedError
  ///
  /// Note:
  ///   You do not have to call this method explicitly, but you must define it. It will be called during the processing of the job.
  #[cfg(feature = "media")]
  fn process_frames(
    _self_: PyRef<'_, Self>,
    _job_id: Py<PyAny>,
    _stream_index: Py<PyAny>,
    _frames: Py<PyAny>,
  ) -> PyResult<PyObject> {
    Err(PyNotImplementedError::new_err(
      "Init process method must be implemented",
    ))
  }

  /// Function called at the end of the process. It might be used to clean up some variables or anything else related to the process.
  ///
  /// Note:
  ///   This method is optional.
  #[cfg(feature = "media")]
  fn ending_process(_self_: PyRef<'_, Self>) -> PyResult<()> {
    Ok(())
  }

  /// Method called for starting the worker. Once called, the worker will automatically start listening to new orders to process.
  ///
  /// This is the only method you will have to call explicitly, other methods will be called directly by the SDK.
  ///
  /// Warning:
  ///   This method must not be re-implemented.
  fn start(self_: PyRef<Self>, py: Python<'_>) {
    let params = self_.parameters.as_ref().unwrap().clone();
    let description = self_.description.as_ref().unwrap().clone();
    let worker = self_.into_py(py);

    py.allow_threads(|| {
      let wrapper = WorkerInstance::new(worker, params, description);
      start_worker(wrapper);
    });
  }
}
