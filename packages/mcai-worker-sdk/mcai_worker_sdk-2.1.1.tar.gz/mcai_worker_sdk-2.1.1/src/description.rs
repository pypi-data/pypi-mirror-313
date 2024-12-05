use mcai_worker_sdk::prelude::*;
use pyo3::prelude::{PyAnyMethods, PyModule};
use pyo3::{pyclass, pymethods, Bound, PyAny, PyResult};
use pyproject_toml::PyProjectToml;
use regex::Regex;

/// Description of the worker. The fields are automatically bound to the information contained in the pyproject.toml file when instantiating the class.
///
/// Arguments:
///   package_name (str): The name of the package.
///
/// Examples:
///   >>> desc = mcai.WorkerDescription(__package__)
#[pyclass(subclass)]
#[derive(Clone, Debug, Default)]
pub struct WorkerDescription {
  /// Name of the worker.
  ///
  /// Bound to the field `name <https://peps.python.org/pep-0621/#name>`_ of the pyproject.toml.
  #[pyo3(get, set)]
  name: String,
  /// Version of the worker.
  ///
  /// Bound to the field `version <https://peps.python.org/pep-0621/#version>`_ of the pyproject.toml.
  #[pyo3(get, set)]
  version: String,
  /// Description of the worker.
  ///
  /// Bound to the field `description <https://peps.python.org/pep-0621/#description>`_ of the pyproject.toml.
  #[pyo3(get, set)]
  description: String,
  /// License of the worker.
  ///
  /// Bound to the field `license <https://peps.python.org/pep-0621/#license>`_ of the pyproject.toml.
  #[pyo3(get, set)]
  license: String,
}

pub fn parse_worker_version(version: String) -> String {
  let semver_re: Regex = Regex::new(r"^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$").unwrap();
  let pep440_re = Regex::new(r"^(?:(?:(?P<epoch>[0-9]+)!)?(?P<release>[0-9]+(?:\.[0-9]+)*)(?P<pre>[-_\.]?(?P<pre_l>(a|b|c|rc|alpha|beta|pre|preview))[-_\.]?(?P<pre_n>[0-9]+)?)?(?P<post>(?:-(?P<post_n1>[0-9]+))|(?:[-_\.]?(?P<post_l>post|rev|r)[-_\.]?(?P<post_n2>[0-9]+)?))?(?P<dev>[-_\.]?(?P<dev_l>dev)[-_\.]?(?P<dev_n>[0-9]+)?)?)(?:\+(?P<local>[a-z0-9]+(?:[-_\.][a-z0-9]+)*))?$").unwrap();
  let pep440_match: bool = pep440_re.is_match(&version);
  let semver_match: bool = semver_re.is_match(&version);
  if pep440_match || semver_match {
    version
  } else {
    panic!("The worker version does not conform to SemVer or PEP440 standards.");
  }
}

#[test]
#[should_panic(expected = "The worker version does not conform to SemVer or PEP440 standards.")]
pub fn test_incorrect_version_parsing() {
  let incorrect_semver_versions = vec![
    "1.2.3-0123".to_string(),
    "1.2.3-0123.0123".to_string(),
    "1.1.2+.123".to_string(),
    "+invalid".to_string(),
    "-invalid".to_string(),
    "-invalid+invalid".to_string(),
    "-invalid.01".to_string(),
    "alpha".to_string(),
    "alpha.beta".to_string(),
    "alpha.beta.1".to_string(),
    "alpha.1".to_string(),
    "alpha+beta".to_string(),
    "alpha_beta".to_string(),
    "alpha.".to_string(),
    "alpha..".to_string(),
    "beta".to_string(),
    "1.0.0-alpha_beta".to_string(),
    "-alpha.".to_string(),
    "1.0.0-alpha..".to_string(),
    "1.0.0-alpha..1".to_string(),
    "1.0.0-alpha...1".to_string(),
    "1.0.0-alpha....1".to_string(),
    "1.0.0-alpha.....1".to_string(),
    "1.0.0-alpha......1".to_string(),
    "1.0.0-alpha.......1".to_string(),
    "01.1.1".to_string(),
    "1.01.1".to_string(),
    "1.1.01".to_string(),
    "1.2".to_string(),
    "1.2.3.DEV".to_string(),
    "1.2-SNAPSHOT".to_string(),
    "1.2.31.2.3----RC-SNAPSHOT.12.09.1--..12+788".to_string(),
    "1.2-RC-SNAPSHOT".to_string(),
    "-1.0.3-gamma+b7718".to_string(),
    "+justmeta".to_string(),
    "9.8.7+meta+meta".to_string(),
    "9.8.7-whatever+meta+meta".to_string(),
    "99999999999999999999999.999999999999999999.99999999999999999----RC-SNAPSHOT.12.09.1--------------------------------..12".to_string(),
  ];
  for version in incorrect_semver_versions.into_iter() {
    parse_worker_version(version);
  }
}

#[test]
pub fn test_semver_version_parsing() {
  let valid_semver_versions = vec![
    "0.0.4".to_string(),
    "1.2.3".to_string(),
    "10.20.30".to_string(),
    "1.1.2-prerelease+meta".to_string(),
    "1.1.2+meta".to_string(),
    "1.1.2+meta-valid".to_string(),
    "1.0.0-alpha".to_string(),
    "1.0.0-beta".to_string(),
    "1.0.0-alpha.beta".to_string(),
    "1.0.0-alpha.beta.1".to_string(),
    "1.0.0-alpha.1".to_string(),
    "1.0.0-alpha0.valid".to_string(),
    "1.0.0-alpha.0valid".to_string(),
    "1.0.0-alpha-a.b-c-somethinglong+build.1-aef.1-its-okay".to_string(),
    "1.0.0-rc.1+build.1".to_string(),
    "2.0.0-rc.1+build.123".to_string(),
    "1.2.3-beta".to_string(),
    "10.2.3-DEV-SNAPSHOT".to_string(),
    "1.2.3-SNAPSHOT-123".to_string(),
    "1.0.0".to_string(),
    "2.0.0".to_string(),
    "1.1.7".to_string(),
    "2.0.0+build.1848".to_string(),
    "2.0.1-alpha.1227".to_string(),
    "1.0.0-alpha+beta".to_string(),
    "1.2.3----RC-SNAPSHOT.12.9.1--.12+788".to_string(),
    "1.2.3----R-S.12.9.1--.12+meta".to_string(),
    "1.2.3----RC-SNAPSHOT.12.9.1--.12".to_string(),
    "1.0.0+0.build.1-rc.10000aaa-kk-0.1".to_string(),
    "99999999999999999999999.999999999999999999.99999999999999999".to_string(),
    "1.0.0-0A.is.legal".to_string(),
  ];
  for version in valid_semver_versions.into_iter() {
    assert_eq!(parse_worker_version(version.clone()), version);
  }
}

#[test]
pub fn test_pep440_version_parsing() {
  let valid_semver_versions = vec![
    "2012.4".to_string(),
    "2012.10".to_string(),
    "1!1.0".to_string(),
    "1!1.1".to_string(),
    "1!2.0".to_string(),
    "0.9.1".to_string(),
    "1.0a1".to_string(),
    "1.0b1".to_string(),
    "1.0rc1".to_string(),
    "1.0.dev1".to_string(),
    "1.0b2.post345.dev456".to_string(),
    "1.0b2.post345".to_string(),
    "1.0rc1.dev456".to_string(),
    "1.0c2".to_string(),
    "1.0.post1".to_string(),
    "1.1.dev1".to_string(),
    "1.1a1".to_string(),
    "0.1.1.dev1+gdcec07a".to_string(),
  ];
  for version in valid_semver_versions.into_iter() {
    assert_eq!(parse_worker_version(version.clone()), version);
  }
}

#[pymethods]
impl WorkerDescription {
  #[new]
  fn new(package: &Bound<'_, PyAny>) -> PyResult<WorkerDescription> {
    if package.is_none() {
      // This means the worker hasn't been packaged and we need to get info through pyproject.toml

      let content = std::fs::read_to_string("./pyproject.toml")
        .map_err(|error| {
          format!(
            "Python Worker must be described by a 'pyproject.toml' file: {}",
            error
          )
        })
        .unwrap();

      let pyproject = PyProjectToml::new(&content)
        .map_err(|error| format!("Could not parse 'pyproject.toml' file: {}", error))
        .unwrap();

      let project = pyproject
        .project
        .expect("The 'pyproject.toml' must contain a 'project' section.");

      Ok(Self {
        name: project.name,
        version: project
          .version
          .expect("Version field must be present in pyproject.toml"),
        description: project.description.unwrap_or_default(),
        license: project
          .license
          .expect("License field must be present in pyproject.toml")
          .text
          .unwrap_or_default(),
      })
    } else {
      let py = package.py();

      let importlib_metadata = PyModule::import_bound(py, "importlib.metadata")?;
      let package_info = importlib_metadata.getattr("metadata")?.call1((package,))?;

      Ok(Self {
        name: package_info.get_item("name")?.to_string(),
        version: package_info.get_item("version")?.to_string(),
        description: package_info.get_item("summary")?.to_string(),
        license: package_info.get_item("license")?.to_string(),
      })
    }
  }
}

impl McaiWorkerDescription for WorkerDescription {
  fn get_name(&self) -> String {
    self.name.clone()
  }

  fn get_description(&self) -> String {
    self.description.clone()
  }

  fn get_version(&self) -> String {
    parse_worker_version(self.version.clone())
  }

  fn get_license(&self) -> McaiWorkerLicense {
    McaiWorkerLicense::new(&self.license)
  }
}

#[test]
fn test_worker_description() {
  use pyo3::marker::Python;

  pyo3::prepare_freethreaded_python();
  let worker_description =
    Python::with_gil(|py| WorkerDescription::new(Python::None(py).bind(py)).unwrap());

  assert_eq!(
    worker_description.get_description(),
    env!("CARGO_PKG_DESCRIPTION")
  );
  assert_eq!(
    worker_description.get_license(),
    McaiWorkerLicense::new(env!("CARGO_PKG_LICENSE"))
  );

  assert_eq!(
    worker_description.get_version(),
    (env!("CARGO_PKG_VERSION"))
  );

  #[cfg(feature = "media")]
  assert_eq!(
    format!("py_{}", worker_description.get_name()),
    format!("{}_media", env!("CARGO_PKG_NAME"))
  );

  #[cfg(not(feature = "media"))]
  assert_eq!(
    format!("py_{}", worker_description.get_name()),
    env!("CARGO_PKG_NAME")
  );
}
