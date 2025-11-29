# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Initial project structure
- `khipu_demo` package with mock clients
- Data provenance tracking
- Synthetic data generators
- Accessible visualization utilities
- First notebook: Metro Housing-Wage Divergence
- Notebook template
- CI/CD pipeline with secret scanning
- Docker and Binder deployment configs
- MkDocs documentation site

### Security

- No secrets or credentials in repository
- Automated secret scanning in CI
- DEMO_MODE enabled by default

## [0.1.0] - 2025-01-15

### Added

- Initial release
- Core `khipu_demo` package
- Mock API clients:
  - BLSMockClient
  - BEAMockClient
  - CensusMockClient
  - EPAMockClient
  - CDCMockClient
  - ZillowMockClient
- Synthetic data generators:
  - Housing-wage panel data
  - Gentrification signals
- Visualization utilities:
  - Colorblind-safe palettes
  - WCAG contrast checker
  - Chart creation helpers
- Notebook #1: Metro Housing-Wage Divergence

[Unreleased]: https://github.com/KR-Labs/khipu-showcase/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/KR-Labs/khipu-showcase/releases/tag/v0.1.0
