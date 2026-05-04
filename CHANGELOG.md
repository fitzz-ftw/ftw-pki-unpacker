# Changelog

All notable changes to this project will be documented in this file.
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
