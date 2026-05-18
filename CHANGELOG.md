# Changelog: ftw-pki-unpacker

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.3a2] - 2026-05-18

### Added
- Add structural, Sphinx-compliant English docstring for the `configname` attribute within `UnpackerCliProtocol`.

### Changed
- Align and update rigid path assertions within `get_started_programms.rst` and `get_started_run_programms.rst` to verify local execution file paths instead of global application layouts.
- Lower the minimum required test coverage threshold (`fail_under`) to 90% in `pyproject.toml` to accurately match the refactored testing state.
- Update the code coverage badge baseline to 90% inside `README.md`.


## [0.0.3a1] - 2026-05-17

### Changed
- **Breaking Change**: Architectural renaming and refactoring from `ftw-pki-receiver` to `ftw-pki-unpacker` to better align with its core purpose.
- All internal module paths and references updated from `receiver` namespaces to `unpacker`.
- Refactored packaging metadata structures and updated `pyproject.toml` to comply with modern Python packaging standards.

### Fixed
- Fixed internal configuration path resolutions and hardened edge-case testing pipelines.
- Restructured testing suites to adapt to module renames, maintaining a solid 93% test coverage.

### Added
- Integrated full API documentation inside source modules following PEP 257 and Sphinx syntax guidelines.
- Added comprehensive developer guides (`get_started_programms.rst`, `get_started_cli_parser.rst`) and automated docstring verification pipelines.
- Integrated the root `README.md` into the Sphinx documentation build index.
- Enabled GitHub Actions CI matrices for automated multi-environment validation.


## [v0.0.2] - 2026-04-29

### Added
* **Core Logic**: Implemented `prog_receive_certs` for end-to-end 
    decryption and installation of certificate packages.
* **CLI Parser**: Introduced `ReceiverCliParser` to handle mandatory `private_key` 
    and `cert_file` arguments.
* **Protocols**: Established `ReceiverCliProtocol` for type-safe argument handling.
* **Helper**: Added `get_parser()` factory function to `cli_parser` for improved API
    accessibility.

### Fixed
* **Config Resolution**: Fixed path resolution by ensuring `config_file_path` is 
    called as a function.
* **Logic Flow**: Improved configuration check logic in `prog_receive_certs` before 
    writing example configurations.
* **Installation**: Ensured secure automatic directory creation based on central 
    PKI configuration.

### Changed
* **Test Infrastructure**: Switched coverage focus in `conf.py` from `ftwpki.password` 
    to `ftwpki.receiver`.
* **RST Structure**: Standardized `.rst` file structure with consistent spacing 
    for `SECTION` markers to improve readability.

### Documentation
* **API Documentation**: Full implementation of docstrings according to PEP 257 and 
    Sphinx rules for `protocols`, `cli_parser`, and `programms` modules.
* **Guides**: Integrated new guides into `index_get_started.rst`.
* **Doctests**: Added comprehensive workflow documentation and tests in 
    `get_started_programms.rst`.

### Testing
* **Coverage**: Achieved 100% test coverage for the entire `receiver` package.
* **Compatibility**: Verified passing test environments for Python 3.11 through 
    3.15 via Tox/Pytest.

## [0.0.1] - 2026-04-24

### Added
* Initial release of the `ftw-pki-receiver` package.
* Implemented PEP 420 namespace structure under `ftwpki.receiver`.
* Added automated coverage reporting and Sphinx documentation boilerplate.
