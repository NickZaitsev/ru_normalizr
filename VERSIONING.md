# Versioning Policy

`ru-normalizr` follows Semantic Versioning.

## Version format

`MAJOR.MINOR.PATCH`

Examples:
- `0.1.0`
- `0.2.0`
- `0.2.1`
- `1.0.0`

## Meaning

- `PATCH`: bug fixes, packaging fixes, documentation-only updates, or behavior corrections that do not intentionally change the public API shape.
- `MINOR`: new public options, new supported normalization features, new CLI flags, or new stage APIs added in a backward-compatible way.
- `MAJOR`: breaking public API changes, changed defaults, removed options, reordered exposed stage semantics, or intentional normalization output changes that break compatibility expectations.

## Pre-1.0 guidance

Until `1.0.0`, minor versions may still include behavior changes while the public contract is being stabilized. The goal before `1.0.0` is:
- lock down default normalization behavior
- stabilize option naming
- stabilize packaging and CLI shape

## Release rules

- Every release updates `ru_normalizr/__init__.py` and `ru_normalizr/pyproject.toml`.
- Every release adds a changelog entry.
- Any intentional normalization output change must be covered by tests and called out in `CHANGELOG.md`.
