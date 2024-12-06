# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html)[^1].

<!---
Types of changes

- Added for new features.
- Changed for changes in existing functionality.
- Deprecated for soon-to-be removed features.
- Removed for now removed features.
- Fixed for any bug fixes.
- Security in case of vulnerabilities.

-->

## [Unreleased]

## [1.0.1] - 2024-12-04

### Fixed

* Updating the target file if it already exists will now work.

## [1.0.0] - 2024-11-15

### Added

* In Task Manager, you can specify publishing relationships to a default file.
* These relationships are used in the `PublishNextTask` action, in order to copies the latest published revision of a file to a target task and file as the base revision.
