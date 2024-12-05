use pyo3::prelude::*;

mod callback;
mod description;
mod helper;
mod instance;
mod logger;
mod parameters;
mod worker;

#[cfg(feature = "media")]
mod media;

pub const WORKER_METHOD_INIT: &str = "setup";

#[cfg(not(feature = "media"))]
pub const WORKER_METHOD_PROCESS: &str = "process";

#[pymodule]
#[pyo3(name = "mcai_worker_sdk")]
fn py_mcai_worker_sdk(py: Python, m: &Bound<'_, PyModule>) -> PyResult<()> {
  m.add("__version__", env!("CARGO_PKG_VERSION"))?;

  m.add_class::<worker::Worker>()?;
  m.add_class::<parameters::WorkerParameters>()?;
  m.add_class::<description::WorkerDescription>()?;
  m.add_class::<callback::CallbackHandle>()?;
  m.add_class::<callback::PythonJobStatus>()?;

  #[cfg(feature = "media")]
  {
    m.add_class::<media::PyGenericFilter>()?;
    m.add_class::<media::Frame>()?;
    m.add_class::<media::FormatContext>()?;
    m.add_class::<media::StreamDescriptor>()?;
    m.add_class::<media::AudioStreamDescriptor>()?;
    m.add_class::<media::DataStreamDescriptor>()?;
    m.add_class::<media::VideoStreamDescriptor>()?;
  }

  logger::setup_logging(py)?;

  Ok(())
}
