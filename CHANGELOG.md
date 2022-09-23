# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2022-09-23
### Added
- Add notification about status of the `nextcloud_install` script.

### Changed
- Handle exit code of `nextcloud_install` script and return result regardless of
  success or failure.
- Run `nextcloud_install` script on background and let the script report progress
  of nextcloud configure phase via WebSocket notifications.
- Migrate CHANGELOG to [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) style.

## [0.1] - 2020-09-22
### Added
- initial release as standalone module.
