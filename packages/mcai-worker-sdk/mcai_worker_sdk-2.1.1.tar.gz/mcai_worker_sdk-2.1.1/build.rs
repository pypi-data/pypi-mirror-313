use serde::Serialize;
use std::{env, fs::File, io::Write};
use toml::{value::Table, Value};

#[derive(Serialize)]
struct PyProjectToml {
  project: Project,
  #[serde(rename = "build-system")]
  build_system: BuildSystem,
}

#[derive(Serialize)]
struct Project {
  name: String,
  description: String,
  repository: String,
  version: String,
  readme: String,
  #[serde(rename = "requires-python")]
  requires_python: String,
  dependencies: Vec<String>,
  license: Table,
  urls: Table,
}

impl Project {
  fn new_from_env() -> Self {
    let mut license = Table::new();
    license.insert(
      "text".to_string(),
      Value::try_from(env::var("CARGO_PKG_LICENSE").unwrap()).unwrap(),
    );

    let mut urls = Table::new();

    if let Ok(feat) = env::var("CARGO_FEATURE_MEDIA") {
      if feat == "1" {
        urls.insert(
          "Documentation".to_string(),
          Value::try_from("https://mcai-python-sdk-media.readthedocs.io/").unwrap(),
        );
      }
    } else {
      urls.insert(
        "Documentation".to_string(),
        Value::try_from("https://mcai-python-sdk.readthedocs.io/").unwrap(),
      );
    }

    Project {
      name: "mcai_worker_sdk".to_string(),
      description: env::var("CARGO_PKG_DESCRIPTION").unwrap(),
      repository: env::var("CARGO_PKG_REPOSITORY").unwrap(),
      version: env::var("CARGO_PKG_VERSION").unwrap(),
      readme: "README.md".to_string(),
      requires_python: ">=3.8".to_string(),
      dependencies: Vec::from(["json-strong-typing".to_string()]),
      license,
      urls,
    }
  }
}

#[derive(Serialize)]
struct BuildSystem {
  requires: Vec<String>,
  #[serde(rename = "build-backend")]
  build_backend: String,
}

impl Default for BuildSystem {
  fn default() -> Self {
    BuildSystem {
      requires: Vec::from(["maturin>=0.13,<0.14".to_string()]),
      build_backend: "maturin".to_string(),
    }
  }
}

fn main() {
  let mut project = Project::new_from_env();
  let build_system = BuildSystem::default();

  if let Ok(feat) = env::var("CARGO_FEATURE_MEDIA") {
    if feat == "1" {
      project.name = format!("{}_media", project.name);
    }
  }

  let pyproject = PyProjectToml {
    project,
    build_system,
  };

  let mut file = File::create("pyproject.toml").unwrap();

  let pyproject = toml::to_string(&pyproject).unwrap();
  file.write_all(pyproject.as_ref()).unwrap();
}
