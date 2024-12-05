#[cfg(not(feature = "media"))]
use mcai_worker_sdk::prelude::Parameter;
#[cfg(not(feature = "media"))]
use pyo3::types::{PyInt, PyList, PyString};
use pyo3::{prelude::*, types::PyDict};

#[cfg(not(feature = "media"))]
pub fn get_destination_paths(response: &Bound<'_, PyAny>) -> Option<Vec<String>> {
  response.downcast::<PyDict>().ok().and_then(|object| {
    object
      .get_item("destination_paths")
      .ok()
      .flatten()
      .and_then(|response_paths| {
        response_paths.downcast::<PyList>().ok().map(|path_list| {
          path_list
            .iter()
            .filter_map(|item| item.downcast::<PyString>().ok().map(ToString::to_string))
            .collect()
        })
      })
  })
}

#[cfg(not(feature = "media"))]
fn parse_string_parameter(dict: &Bound<'_, PyDict>, key: &str) -> Option<String> {
  dict
    .get_item(key)
    .map(|result| result.map(|value| value.to_string()))
    .unwrap_or(None)
}

#[cfg(not(feature = "media"))]
fn parse_value_parameter(
  dict: &Bound<'_, PyDict>,
  key: &str,
  kind: String,
) -> Option<serde_json::Value> {
  if let Ok(Some(value)) = dict.get_item(key) {
    match &kind[..] {
      "boolean" => Some(serde_json::Value::Bool(
        value.to_string().parse::<bool>().unwrap(),
      )),
      "int" => Some(serde_json::Value::Number(
        value.to_string().parse::<i64>().unwrap().into(),
      )),
      "string" => Some(serde_json::Value::String(value.to_string())),
      "array_of_strings" | "array_of_templates" => Some(serde_json::Value::Array(
        value
          .iter()
          .ok()?
          .filter_map(|i| i.ok())
          .filter_map(|i| {
            if let Ok(value) = i.downcast::<PyString>() {
              Some(value.clone())
            } else {
              None
            }
          })
          .map(|i_as_value| serde_json::Value::String(i_as_value.to_string()))
          .collect(),
      )),
      "array_of_ints" => Some(serde_json::Value::Array(
        value
          .iter()
          .ok()?
          .filter_map(|i| i.ok())
          .filter_map(|i| {
            if let Ok(value) = i.downcast::<PyInt>() {
              Some(value.clone())
            } else {
              None
            }
          })
          .map(|i_as_value| {
            serde_json::Value::Number(i_as_value.to_string().parse::<i64>().unwrap().into())
          })
          .collect(),
      )),
      _ => {
        mcai_worker_sdk::prelude::error!("Invalid Parameter Type");
        None
      }
    }
  } else {
    None
  }
}

#[cfg(not(feature = "media"))]
pub fn get_parameters(response: &Bound<'_, PyAny>) -> Option<Vec<Parameter>> {
  if response.is_none() {
    return None;
  }

  response
    .downcast::<PyDict>()
    .map(|object| {
      object
        .get_item("parameters")
        .unwrap_or(None)
        .and_then(|parameters| {
          parameters
            .downcast::<PyList>()
            .map(|params_list| {
              let parameters: Vec<Parameter> = params_list
                .iter()
                .filter_map(|i| {
                  if let Ok(value) = i.downcast::<PyDict>() {
                    Some(value.clone())
                  } else {
                    None
                  }
                })
                .filter_map(
                  |param| match (param.get_item("id"), param.get_item("kind")) {
                    (Ok(Some(v)), Ok(Some(w))) => Some(Parameter {
                      id: v.to_string(),
                      kind: w.to_string(),
                      store: parse_string_parameter(&param, "store"),
                      value: parse_value_parameter(&param, "value", w.to_string()),
                      default: parse_value_parameter(&param, "default", w.to_string()),
                    }),
                    _ => None,
                  },
                )
                .collect();

              Some(parameters)
            })
            .unwrap_or(None)
        })
    })
    .unwrap_or(None)
}

pub fn handle_automatic_job_parameters(
  py: Python,
  parameters_schema: &Bound<'_, PyAny>,
) -> PyResult<Py<PyDict>> {
  let parameters_schema_extended = parameters_schema.extract::<Py<PyDict>>()?;

  let requirements_type = PyDict::new_bound(py);
  requirements_type.set_item("type", "object")?;

  parameters_schema_extended
    .bind(py)
    .get_item("properties")?
    .unwrap()
    .set_item("requirements", requirements_type)?;

  let source_paths_items_type = PyDict::new_bound(py);
  source_paths_items_type.set_item("type", "string")?;

  let source_paths_type = PyDict::new_bound(py);
  source_paths_type.set_item("type", "array")?;
  source_paths_type.set_item("items", source_paths_items_type)?;

  parameters_schema_extended
    .bind(py)
    .get_item("properties")?
    .unwrap()
    .set_item("source_paths", source_paths_type)?;

  Ok(parameters_schema_extended)
}

#[test]
#[cfg(not(feature = "media"))]
pub fn test_get_destination_paths() {
  pyo3::prepare_freethreaded_python();

  Python::with_gil(|py| {
    let destination_paths = vec![
      "/path/to/destination/file_1".to_string(),
      "/path/to/destination/file_2".to_string(),
      "/path/to/destination/file_3".to_string(),
    ];

    let py_list = PyList::new_bound(py, destination_paths.clone());
    let py_dict = PyDict::new_bound(py);
    let result = py_dict.set_item("destination_paths", py_list);
    assert!(result.is_ok());

    let py_any: &Bound<'_, PyAny> = &py_dict.into_any();

    let result = get_destination_paths(py_any);
    assert!(result.is_some());
    assert_eq!(destination_paths, result.unwrap());
  });
}

#[test]
#[cfg(not(feature = "media"))]
pub fn test_get_destination_paths_without_key() {
  pyo3::prepare_freethreaded_python();

  Python::with_gil(|py| {
    let py_dict = PyDict::new_bound(py);

    let py_any: &Bound<'_, PyAny> = &py_dict.into_any();

    let result = get_destination_paths(py_any);
    assert!(result.is_none());
  });
}

#[test]
#[cfg(not(feature = "media"))]
pub fn test_get_destination_paths_without_list_value() {
  pyo3::prepare_freethreaded_python();

  Python::with_gil(|py| {
    let py_dict = PyDict::new_bound(py);
    let result = py_dict.set_item("destination_paths", "some_value");
    assert!(result.is_ok());

    let py_any: &Bound<'_, PyAny> = &py_dict.into_any();

    let result = get_destination_paths(py_any);
    assert!(result.is_none());
  });
}
