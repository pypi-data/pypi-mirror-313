use crate::helper::handle_automatic_job_parameters;

use jsonschema::JSONSchema;
use mcai_worker_sdk::prelude::*;
use pyo3::{
  prelude::*,
  types::{PyDict, PyList, PyType},
};
use schemars::{schema::RootSchema, JsonSchema};
use serde::{Deserialize, Serialize};
use serde_json::Value;
use std::collections::HashMap;

/// Worker parameters base class to extend to define the parameters of your worker.
///
/// Examples:
///   >>> class McaiWorkerParameters(mcai.WorkerParameters):
///   >>>   action: str
///   >>>   number: int
///   >>>   array_of_strings: list[str]
///   >>>   array_of_integers: list[int]
///
/// Note:
///   Some parameters can be declared as optional. Use `Optional <https://docs.python.org/3/library/typing.html#typing.Optional>`_ from typing to do so.
///
/// Note:
///   The parameter class will also have an attribute :attr:`requirements` autogerenated by StepFlow and directly handled by the SDK.
///
/// Warning:
///   You should take special care when defining this class to type properly its attributes.
///   Under the hood, attributes types will be used by the SDK to cast parameters arriving from the backend into their proper Python type.
#[pyclass(subclass)]
#[derive(Clone, Debug, Default, Deserialize, JsonSchema, Serialize)]
pub struct WorkerParameters {
  #[serde(flatten)]
  parameters: HashMap<String, Value>,
}

#[pymethods]
impl WorkerParameters {
  #[new]
  pub(crate) fn new() -> Self {
    WorkerParameters::default()
  }
}

impl WorkerParameters {
  pub(crate) fn get_schema(parameters: &Py<PyType>) -> PyResult<RootSchema> {
    let parameters_schema_as_string = Python::with_gil(|py| -> PyResult<String> {
      let json_module = py.import_bound("json")?;
      let schema_module = py.import_bound("strong_typing.schema")?;

      let parameters_schema = schema_module
        .getattr("classdef_to_schema")?
        .call1((parameters,))?;

      let parameters_schema_extended = handle_automatic_job_parameters(py, &parameters_schema)?;

      json_module
        .getattr("dumps")?
        .call1((parameters_schema_extended,))?
        .extract::<String>()
    })?;

    Ok(
      serde_json::from_str(&parameters_schema_as_string).unwrap_or_else(|error| {
        panic!(
          "Could not deserialize parameters schema: {:?} (schema={})",
          error, parameters_schema_as_string
        )
      }),
    )
  }

  pub(crate) fn to_python_parameters(&self, worker_parameters: &PyObject) -> PyResult<()> {
    for (key, value) in self.parameters.iter() {
      Self::set_value_to_python_type(worker_parameters, key, value)?;
    }
    Ok(())
  }

  pub(crate) fn validate_parameters(&self, parameters_type: &Py<PyType>) -> Result<()> {
    let schema = Self::get_schema(parameters_type).unwrap();
    let schema_json_value = serde_json::to_value(schema)?;
    let json_schema = JSONSchema::compile(&schema_json_value)
      .map_err(|error| MessageError::RuntimeError(error.to_string()))?;

    let parameters_value = serde_json::to_value(self)?;

    json_schema.validate(&parameters_value).map_err(|errors| {
      let mut messages = vec![];
      for error in errors {
        messages.push(error.to_string());
      }
      MessageError::ParameterValueError(format!(
        "Parameters validation errors: {}",
        messages.join(", ")
      ))
    })
  }

  fn set_value_to_python_type(
    worker_parameters: &PyObject,
    key: &str,
    value: &Value,
  ) -> PyResult<()> {
    Python::with_gil(|py| match value {
      Value::Bool(boolean) => worker_parameters.setattr(py, key, *boolean),
      Value::Number(number) => worker_parameters.setattr(py, key, number.as_u64()),
      Value::String(content) => worker_parameters.setattr(py, key, content),
      Value::Array(values) => {
        let list = PyList::empty_bound(py);
        for value in values {
          Self::add_value_to_py_list(value, &list, py)?;
        }

        worker_parameters.setattr(py, key, list)
      }
      Value::Object(map) => {
        let object = PyDict::new_bound(py);
        for (key, value) in map.iter() {
          Self::serde_json_to_pyo3_value(key, value, &object, py)?;
        }
        worker_parameters.setattr(py, key, object)
      }
      _ => Ok(()),
    })
  }

  fn serde_json_to_pyo3_value(
    key: &str,
    value: &Value,
    result: &Bound<'_, PyDict>,
    py: Python,
  ) -> PyResult<()> {
    match value {
      Value::Null => {}
      Value::Bool(boolean) => result.set_item(key, boolean)?,
      Value::Number(number) => result.set_item(key, number.as_u64())?,
      Value::String(content) => result.set_item(key, content)?,
      Value::Array(values) => {
        let list = PyList::empty_bound(py);
        for value in values {
          Self::add_value_to_py_list(value, &list, py)?;
        }

        result.set_item(key, list)?;
      }
      Value::Object(map) => {
        let object = PyDict::new_bound(py);
        for (key, value) in map.iter() {
          Self::serde_json_to_pyo3_value(key, value, &object, py)?;
        }
        result.set_item(key, object)?;
      }
    }
    Ok(())
  }

  fn add_value_to_py_list(value: &Value, list: &Bound<'_, PyList>, py: Python) -> PyResult<()> {
    match value {
      Value::String(string) => {
        list.append(string)?;
      }
      Value::Null => {}
      Value::Bool(boolean) => {
        list.append(boolean)?;
      }
      Value::Number(number) => {
        list.append(number.as_u64())?;
      }
      Value::Array(values) => {
        let sub_list = PyList::empty_bound(py);
        for value in values {
          Self::add_value_to_py_list(value, &sub_list, py)?;
        }
        list.append(sub_list)?;
      }
      Value::Object(map) => {
        let object = PyDict::new_bound(py);
        for (key, value) in map.iter() {
          Self::serde_json_to_pyo3_value(key, value, &object, py)?;
        }
        list.append(object)?;
      }
    }
    Ok(())
  }
}

#[test]
pub fn test_parameters_schema_generation() {
  pyo3::prepare_freethreaded_python();

  Python::with_gil(|py| {
    let parameters: Py<PyType> = PyModule::from_code_bound(
      py,
      "class Parameters:
                string_param: str
                action: str
                number: int
                array_of_strings: list[str]
                array_of_integers: list[int]",
      "",
      "",
    )
    .unwrap()
    .getattr("Parameters")
    .unwrap()
    .extract::<Py<PyType>>()
    .unwrap();

    let schema = serde_json::to_value(&WorkerParameters::get_schema(&parameters).unwrap()).unwrap();

    assert_eq!(
      schema,
      serde_json::json!({
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "required": [
          "action",
          "array_of_integers",
          "array_of_strings",
          "number",
          "string_param"
        ],
        "properties": {
          "action": {
            "type": "string"
          },
          "array_of_integers": {
            "type": "array",
            "items": {
              "type": "integer"
            }
          },
          "array_of_strings": {
            "type": "array",
            "items": {
              "type": "string"
            }
          },
          "number": {
            "type": "integer"
          },
          "string_param": {
            "type": "string"
          },
          "requirements": {
            "type": "object"
          },
          "source_paths": {
            "type": "array",
            "items": {
              "type": "string"
            }
          }
        },
        "additionalProperties": false
      })
    )
  })
}

#[test]
pub fn test_conversion_to_python_parameters() {
  use pyo3::types::{PyInt, PyString};

  pyo3::prepare_freethreaded_python();

  Python::with_gil(|py| {
    let worker_parameters: Py<PyType> = PyModule::from_code_bound(
      py,
      "class Parameters:
                action: str
                number: int
                array_of_strings: list[str]
                array_of_integers: list[int]",
      "",
      "",
    )
    .unwrap()
    .getattr("Parameters")
    .unwrap()
    .extract::<Py<PyType>>()
    .unwrap();

    let injected_parameters = WorkerParameters {
      parameters: HashMap::from([
        ("action".to_string(), Value::from("completed".to_string())),
        ("number".to_string(), Value::from(123)),
        (
          "array_of_strings".to_string(),
          Value::from(Vec::from(["value_1".to_string(), "value_2".to_string()])),
        ),
        (
          "array_of_integers".to_string(),
          Value::from(Vec::from([0, 1, 2, 3, 4, 5, 6])),
        ),
      ]),
    };

    let worker_parameters = worker_parameters.to_object(py);
    injected_parameters
      .to_python_parameters(&worker_parameters)
      .unwrap();

    let action = worker_parameters.getattr(py, "action").unwrap();
    assert!(action.bind(py).is_instance_of::<PyString>());
    assert_eq!(action.bind(py).to_string(), "completed");

    let number = worker_parameters.getattr(py, "number").unwrap();
    assert!(number.bind(py).is_instance_of::<PyInt>());
    assert_eq!(number.bind(py).to_string(), "123");

    let array_of_strings = worker_parameters.getattr(py, "array_of_strings").unwrap();
    assert!(array_of_strings.bind(py).is_instance_of::<PyList>());
    assert_eq!(
      array_of_strings.bind(py).to_string(),
      "['value_1', 'value_2']"
    );

    let array_of_integers = worker_parameters.getattr(py, "array_of_integers").unwrap();
    assert!(array_of_integers.bind(py).is_instance_of::<PyList>());
    assert_eq!(
      array_of_integers.bind(py).to_string(),
      "[0, 1, 2, 3, 4, 5, 6]"
    );
  })
}
