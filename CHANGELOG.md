# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog] and this project adheres to [Semantic Versioning].

<!--
GitHub MD Syntax:
https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax

Highlighting:
https://docs.github.com/assets/cb-41128/mw-1440/images/help/writing/alerts-rendered.webp

> [!NOTE]
> Highlights information that users should take into account, even when skimming.

> [!TIP]
> Optional information to help a user be more successful.

> [!IMPORTANT]
> Crucial information necessary for users to succeed.

> [!WARNING]
> Urgent info that needs immediate user attention to avoid problems.

> [!CAUTION]
> Advised about risks or negative outcomes of certain actions.
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

<!-- Your changes go here -->

### Fixed

- Method `open_ticket` may be static warning
- Compliance check
  - It is enough to check if all characters have been added to the audit module. We
    don't need to check for `is_active()` here, as they will be at some point in the future.

### Changed

- Recruitment thread start text improved

## [1.1.1] - 2026-01-06

### Changed

- Translations updated

## [1.1.0] - 2025-12-02

### Added

- Interaction buttons to the `recruit_me` cog

### Changed

- Translations updated

### Removed

- `allianceauth-app-utils` as dependency

## [1.0.1] - 2025-11-04

### Changed

- Switch to PyPI trusted publishing

### Changed

- Translations updated

## [1.0.0] - 2025-10-07

### Added

- Translations

## [0.11.0] - 2025-07-15

### Added

- Command permissions

### Changed

- Improvements to the `lookup` cog
  - zKillboard statistics improved
  - Output of the `/lookup` command is now ephemeral
  - Several code improvements

## [0.10.0] - 2025-07-13

### Added

- `locate` cog

### Changed

- `discord` imports simplified

## [0.9.0] - 2025-07-10

### Added

- Lookup channels to cog settings

## [0.8.0] - 2025-07-07

### Added

- Plex market to price lookups
- Proper descriptions to slash commands

### Changed

- `price` command group for price checks
- Updated `members` cog and renamed to `lookup`
- `!auth` command to `/auth`
- `!about` command to `/about`
- Improvements to the `admin` cog
- Move class- and static methods to the top of the class in cogs

### Removed

- `timers` cog
- `!orphans` command from `auth` cog
- `!uptime` command from `about` cog

## [0.7.1] - 2025-06-20

### Added

- DB based cog settings

## [0.7.0] - 2025-05-30

### Added

- Models cog

### Changed

- Unload cogs with the same name before loading our own cog

## [0.6.2] - 2025-05-15

### Changed

- Improvements to the `recruit_me` cog
  - Use Enum in bot responses
  - Messages improved

## [0.6.1] - 2025-02-24

### Changed

- Improvements to the `welcome` cog
- Better permission checks for the `recruit_me` cog

## [0.6.0] - 2025-02-20

### Added

- Admin cog
- Recruitment cog
- Welcome cog

### Changed

- `/admin commands` output formatted
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

- Optimized time cog to reduce the number of SQL queries and use Django's own
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

<!-- Links to be updated upon release -->

[0.0.1]: https://github.com/terra-nanotech/tn-nt-discordbot-cogs/commits/v0.0.1 "v0.0.1"
[0.0.2]: https://github.com/terra-nanotech/tn-nt-discordbot-cogs/compare/v0.0.1...v0.0.2 "v0.0.2"
[0.0.3]: https://github.com/terra-nanotech/tn-nt-discordbot-cogs/compare/v0.0.2...v0.0.3 "v0.0.3"
[0.0.4]: https://github.com/terra-nanotech/tn-nt-discordbot-cogs/compare/v0.0.3...v0.0.4 "v0.0.4"
[0.1.0]: https://github.com/terra-nanotech/tn-nt-discordbot-cogs/compare/v0.0.4...v0.1.0 "v0.1.0"
[0.10.0]: https://github.com/terra-nanotech/tn-nt-discordbot-cogs/compare/v0.9.0...v0.10.0 "v0.10.0"
[0.11.0]: https://github.com/terra-nanotech/tn-nt-discordbot-cogs/compare/v0.10.0...v0.11.0 "v0.11.0"
[0.2.0]: https://github.com/terra-nanotech/tn-nt-discordbot-cogs/compare/v0.1.0...v0.2.0 "v0.2.0"
[0.2.1]: https://github.com/terra-nanotech/tn-nt-discordbot-cogs/compare/v0.2.0...v0.2.1 "v0.2.1"
[0.2.2]: https://github.com/terra-nanotech/tn-nt-discordbot-cogs/compare/v0.2.1...v0.2.2 "v0.2.2"
[0.3.0]: https://github.com/terra-nanotech/tn-nt-discordbot-cogs/compare/v0.2.2...v0.3.0 "v0.3.0"
[0.3.1]: https://github.com/terra-nanotech/tn-nt-discordbot-cogs/compare/v0.3.0...v0.3.1 "v0.3.1"
[0.4.0]: https://github.com/terra-nanotech/tn-nt-discordbot-cogs/compare/v0.3.1...v0.4.0 "v0.4.0"
[0.5.0]: https://github.com/terra-nanotech/tn-nt-discordbot-cogs/compare/v0.4.0...v0.5.0 "v0.5.0"
[0.6.0]: https://github.com/terra-nanotech/tn-nt-discordbot-cogs/compare/v0.5.0...v0.6.0 "v0.6.0"
[0.6.1]: https://github.com/terra-nanotech/tn-nt-discordbot-cogs/compare/v0.6.0...v0.6.1 "v0.6.1"
[0.6.2]: https://github.com/terra-nanotech/tn-nt-discordbot-cogs/compare/v0.6.1...v0.6.2 "v0.6.2"
[0.7.0]: https://github.com/terra-nanotech/tn-nt-discordbot-cogs/compare/v0.6.2...v0.7.0 "v0.7.0"
[0.7.1]: https://github.com/terra-nanotech/tn-nt-discordbot-cogs/compare/v0.7.0...v0.7.1 "v0.7.1"
[0.8.0]: https://github.com/terra-nanotech/tn-nt-discordbot-cogs/compare/v0.7.1...v0.8.0 "v0.8.0"
[0.9.0]: https://github.com/terra-nanotech/tn-nt-discordbot-cogs/compare/v0.8.0...v0.9.0 "v0.9.0"
[1.0.0]: https://github.com/ppfeufer/tn-nt-discordbot-cogs/compare/v0.11.0...v1.0.0 "v1.0.0"
[1.0.1]: https://github.com/ppfeufer/tn-nt-discordbot-cogs/compare/v1.0.0...v1.0.1 "v1.0.1"
[1.1.0]: https://github.com/ppfeufer/tn-nt-discordbot-cogs/compare/v1.0.1...v1.1.0 "v1.1.0"
[1.1.1]: https://github.com/ppfeufer/tn-nt-discordbot-cogs/compare/v1.1.0...v1.1.1 "v1.1.1"
[in development]: https://github.com/ppfeufer/tn-nt-discordbot-cogs/compare/v1.1.1...HEAD "In Development"
[keep a changelog]: http://keepachangelog.com/ "Keep a Changelog"
[semantic versioning]: http://semver.org/ "Semantic Versioning"
