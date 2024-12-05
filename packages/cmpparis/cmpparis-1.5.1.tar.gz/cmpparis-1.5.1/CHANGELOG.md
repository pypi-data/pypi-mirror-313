# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.5.1] - 2024-12-03

### Added
- Add upload function to FTP class

### Changed
- Nothing

### Fixed
- Nothing

## [1.4.1] - 2024-11-07

### Added
- Add class to interact with Sharepoint

### Changed
- Nothing

### Fixed
- Nothing

## [1.3.1] - 2024-10-10

### Added
- Add mssql class to connect to Microsoft SQL Servers databases

### Changed
- Nothing

### Fixed
- Nothing

## [1.2.1] - 2024-10-04

### Added
- Nothing

### Changed
- Add missing disconnect function to odbc

### Fixed
- Removed `from_email` and `to_email` parameters from the function signature
- Now uses a generic error email address for `from_email`, retrieved from the parameter store
- Support email address (`to_email`) is now passed directly to the function, retrieved from the parameter store

## [1.1.0] - 2024-09-27

### Added
- Nothing

### Changed
- Nothing

### Fixed
- Fixed get_parameter function: Added verification condition to decrypt the password

## [1.2.0] - 2024-09-30

### Added
- Added SqlFactory and Odbc classes: Allows connection to Microsoft Server databases

### Changed
- Nothing

### Fixed
- Nothing

## [1.1.0] - 2024-09-27

### Added
- Nothing

### Changed
- Nothing

### Fixed
- Fixed get_parameter function: Added verification condition to decrypt the password

## [1.0.0] - 2024-09-23

### Added
- Added FTP functions
- Added S3 functions
- Added MongoDB functions
- Added SES functions
- Added utils functions

### Changed
- Nothing

### Fixed
- Nothing

## [0.1.1] - 2024-09-02

### Added
- Added and tested initial functions to get started with PyPI

### Changed
- Nothing

### Fixed
- Nothing

## [0.0.1] - 2024-09-02

### Added
- Initial project setup