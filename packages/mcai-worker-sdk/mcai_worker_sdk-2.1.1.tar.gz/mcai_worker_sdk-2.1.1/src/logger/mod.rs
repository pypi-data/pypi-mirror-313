use mcai_worker_sdk::prelude::*;
use pyo3::{prelude::*, types::PyDict};

pub const WORKER_LOG_LEVEL_DEBUG: &str = "DEBUG";
pub const WORKER_LOG_LEVEL_INFO: &str = "INFO";
pub const WORKER_LOG_LEVEL_WARNING: &str = "WARNING";
pub const WORKER_LOG_LEVEL_ERROR: &str = "ERROR";
pub const WORKER_LOG_LEVEL_CRITICAL: &str = "CRITICAL";
pub const LOG_LEVEL_ENV_VAR: &str = "MCAI_LOG";

#[pyfunction]
fn bind_logs_to_rust(record: &Bound<'_, PyAny>) -> PyResult<()> {
  let level = record.getattr("levelname")?.extract::<String>()?;
  let message = record.getattr("getMessage")?.call0()?.extract::<String>()?;

  match level.as_str() {
    WORKER_LOG_LEVEL_DEBUG => debug!("{}", message),
    WORKER_LOG_LEVEL_INFO => info!("{}", message),
    WORKER_LOG_LEVEL_WARNING => warn!("{}", message),
    WORKER_LOG_LEVEL_ERROR => error!("{}", message),
    WORKER_LOG_LEVEL_CRITICAL => error!("{}", message),
    _ => {}
  }
  Ok(())
}

pub fn setup_logging(py: Python) -> PyResult<()> {
  let logging = py.import_bound("logging")?;
  logging.setattr(
    "bind_logs_to_rust",
    wrap_pyfunction!(bind_logs_to_rust, logging.clone())?,
  )?;

  // Define our new handler that throw logs to bind_logs_to_rust function
  py.run_bound(
    include_str!("mcai_logs_handler.py"),
    Some(&logging.dict()),
    None,
  )?;

  let kwargs = PyDict::new_bound(py);
  kwargs.set_item(
    "level",
    std::env::var(LOG_LEVEL_ENV_VAR)
      .unwrap_or_else(|_| WORKER_LOG_LEVEL_WARNING.to_string())
      .to_uppercase(),
  )?;
  kwargs.set_item("handlers", [logging.getattr("McaiLogsHandler")?.call0()?])?;

  logging.getattr("basicConfig")?.call((), Some(&kwargs))?;

  Ok(())
}
