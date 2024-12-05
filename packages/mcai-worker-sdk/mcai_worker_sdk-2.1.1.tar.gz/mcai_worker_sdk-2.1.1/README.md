# Python SDK for Media Cloud AI workers

Based on [mcai_worker_sdk](https://gitlab.com/media-cloud-ai/sdks/rs_mcai_worker_sdk), this SDK uses the [PyO3 crate](https://github.com/PyO3/pyo3) to export a compiled module compatible with CPython ABI.

## Documentation

Please, check the docs [here](https://media-cloud-ai.gitlab.io/sdks/py_mcai_worker_sdk/mcai_worker_sdk/) and [here](https://media-cloud-ai.gitlab.io/sdks/py_mcai_worker_sdk/mcai_worker_sdk_media/) for the SDK with the media feature enabled.

## Build

Before using the Python module you should build it as a CPython library. This will require a virtualenv (where the module will be installed) and [maturin](https://github.com/PyO3/maturin) to compile the module.

```bash
virtualenv venv # Create your environment
source venv/bin/activate # Launch it
```

You can then either build the module in development mode (this will build and install the module in your virtualenv):

```bash
maturin develop --features extension-module # Build and install the module
```

Or build the wheel file and install it manually via `pip`:

```bash
maturin build --features extension-module # Build the wheel file to install the module
pip install path/to/generated/wheel/file
```

You will now be able to import the module in your Python's scripts by doing:

```python
import mcai_worker_sdk as mcai
```

Check out [maturin's docs](https://www.maturin.rs/distribution.html#build-wheels) for more information on building the module!

### Supported version

We intempt to support as many distribution and architecture as we can, however if `pip` doesn't find any compatible version for your installation it will download the source and try to compile them directly.

This operation supposes that you have at least __Rust 1.62__.

We currently support the following version of Python implementations:
- [x] CPython 3.8 : manylinux
- [x] CPython 3.9 : manylinux, macosx x86_64
- [x] CPython 3.10 : manylinux, macosx x86_64, macosx arm64
- [x] CPython 3.11 : manylinux, macosx arm54
- [x] Pypy 3.8 : manylinux
- [x] Pypy 3.9 : manylinux

And the following core architectures:
- [x] x86_64


## Test

To run tests you must have `json-strong-typing` installed:

```bash
pip install json-strong-typing
```

Then launch tests basically:

```bash
cargo test
cargo test --features media
```

### Running examples

#### Build the Python module

In your virtual environment:

```bash
maturin develop
```

#### Simple worker

```bash
RUST_LOG=debug \
SOURCE_ORDERS="examples/message.json" \
PYTHON_WORKER_FILENAME="worker.py" \
SOURCE_PATH="README.md" \
DESTINATION_PATH="README.md.out" \
python worker.py
```

#### Media worker

First set the media filename:

```bash
export SOURCE_PATH="/folder/filename.ext"
```

Then run the SDK with these parameters:

```bash
RUST_LOG=debug \
SOURCE_ORDERS="examples/message.json" \
PYTHON_WORKER_FILENAME="media_worker.py" \
DESTINATION_PATH="results.json" \
cargo run --features media
```
