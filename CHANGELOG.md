# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

<!--
GitHub MD Syntax:
https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax

Highlighting:
https://docs.github.com/assets/cb-41128/mw-1440/images/help/writing/alerts-rendered.webp

> [!NOTE]
> Highlights information that users should take into account, even when skimming.

> [!IMPORTANT]
> Crucial information necessary for users to succeed.

> [!WARNING]
> Critical content demanding immediate user attention due to potential risks.
-->

## [In Development] - Unreleased

<!--
Section Order:

### Added
### Fixed
### Changed
### Deprecated
### Removed
### Security
-->

### Added

- Admin cog
- Welcome cog

### Changed

- Embed creation for a market moved to its own function
- Switch to slash commands for price checks

## [0.5.0] - 2023-08-01

### Added

- Dependency to `allianceauth-app-utils`

### Fixed

- Pluralization in `price` cog

### Changed

- `about` cog modernised/updated
- `auth` cog modernised/updated
- `members` cog modernised/updated
- `price_check` cog modernised/updated
- `timer` cog modernised/updated

### Removed

- Unnecessary f-strings from `price_check` cog

## [0.4.0] - 2023-07-21

### Added

- Dependency to `django-eveuniverse`

### Changed

- Moved the build process to PEP 621 / pyproject.toml
- Switched to [Fuzzwork Market Data API](https://market.fuzzwork.co.uk/api/) (RIP evepraisal)

## [0.3.1] - 2023-06-27

### Fixed

- Auth link (Thanks Discord for f\*\*king up your MD parser)

## [0.3.0] - 2022-06-16

### Removed

- Time cog. Will be provided by `aa-timezones`

## [0.2.2] - 2022-06-02

### Changed

- Requirements:
  - Allianceauth Discordbot with no version restrictions, since `discordproxy` now
    is compatible with `allianceauth-discordbot` and can use `py-cord>=2`

## [0.2.1] - 2022-02-04

### Changed

- Requirements:
  - Allianceauth Discordbot < 3.0.0 (Until this bug is fixed » https://github.com/pvyParts/allianceauth-discordbot/issues/56)

## [0.2.0] - 2021-12-15

### Added

- Rens, Hek, Dodixie and Perimeter to the overall market list
- Order counts

## [0.1.0] - 2021-11-30

### Changed

- Minimum requirements
  - Python 3.7
  - Alliance Auth v2.9.3
  - Alliance Auth Discordbot v0.5.3

## [0.0.4] - 2021-09-02

### Changed

- Optimized time cogg to reduce the number of SQL queries and use Django's own
  method to determine the URL to the timezones module

## [0.0.3] - 2021-07-20

### Change

- setup.py improved

## [0.0.2] - 2021-07-11

### Fixed

- Build instructions for pypi

## [0.0.1] - 2021-07-11

### Added

- Initial Version
