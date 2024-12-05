<a name="unreleased"></a>
## [Unreleased]


<a name="1.1.3"></a>
## [1.1.3] - 2022-01-26
### Feat
- bump sdk to 1.1.1

### Fix
- add lock file


<a name="1.1.2"></a>
## [1.1.2] - 2022-01-14
### Feat
- bump to 1.1.2


<a name="1.1.2-rc2"></a>
## [1.1.2-rc2] - 2022-01-14
### Feat
- bump to 1.1.2-rc2


<a name="1.1.2-rc1"></a>
## [1.1.2-rc1] - 2022-01-14
### Fix
- correct debian bullseye in dockerfile


<a name="1.1.1"></a>
## [1.1.1] - 2022-01-13
### Feat
- bump buster to rust 1.57
- bump version to 1.1.1
- add bullseye for python3.9

### Fix
- remove lock for safe library push
- remove unnecessary borrow


<a name="1.1.0"></a>
## [1.1.0] - 2021-11-10
### Feat
- bump to sdk version 1.1.0


<a name="1.1.0-rc"></a>
## 1.1.0-rc - 2021-09-16
### CI
- add --allow-releaseinfo-change update for coverage step
- install missing Python dev packages
- use Rust 1.50.0 image for coverage
- Update Gitlab-CI file with common Rust pipelines

### Ci
- add image push to registry

### Feat
- add python3.7 image and job_id in process

### Fix
- fix dockerfile with wrong workdir
- add cargo lock for ci

### Python
- clean worker.py file (and apply pep8 code format)
- remove useless Frame::display() function
- worker init() is optional
- errors and iterators handling refactoring
- move py_error_to_string function to helpers
- fix frame data access
- move out some code to new parameters module
- Update parameter support


[Unreleased]: https://gitlab.com/media-cloud-ai/sdks/py_mcai_worker_sdk/compare/1.1.3...HEAD
[1.1.3]: https://gitlab.com/media-cloud-ai/sdks/py_mcai_worker_sdk/compare/1.1.2...1.1.3
[1.1.2]: https://gitlab.com/media-cloud-ai/sdks/py_mcai_worker_sdk/compare/1.1.2-rc2...1.1.2
[1.1.2-rc2]: https://gitlab.com/media-cloud-ai/sdks/py_mcai_worker_sdk/compare/1.1.2-rc1...1.1.2-rc2
[1.1.2-rc1]: https://gitlab.com/media-cloud-ai/sdks/py_mcai_worker_sdk/compare/1.1.1...1.1.2-rc1
[1.1.1]: https://gitlab.com/media-cloud-ai/sdks/py_mcai_worker_sdk/compare/1.1.0...1.1.1
[1.1.0]: https://gitlab.com/media-cloud-ai/sdks/py_mcai_worker_sdk/compare/1.1.0-rc...1.1.0
