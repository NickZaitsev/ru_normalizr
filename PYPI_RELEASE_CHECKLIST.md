# PyPI Release Checklist

## Before tagging

- Ensure the working tree is in the state you want to publish.
- Review `CHANGELOG.md` and add a release entry.
- Update version in:
  - `__init__.py`
  - `pyproject.toml`
- Confirm `README.md` examples still match actual output.
- Confirm `LICENSE` is present.

## Install tooling

```bash
py -3.12 -m pip install -r requirements-dev.txt
```

## Preferred validation flow

```bash
py -3.12 scripts/dev.py check
```

`check` already runs the full release validation flow:

- `clean`
- version sync check between `__init__.py` and `pyproject.toml`
- `ruff check .`
- `pytest -q`
- fresh build of `dist/*`
- `twine check dist/*`

`clean` inside `check` removes local build/cache junk:

- `build/`
- `dist/`
- `.tmp_dist/`
- `ru_normalizr.egg-info/`
- `.pytest_cache/`
- `.ruff_cache/`
- all `__pycache__/`
- dictionary cache files like `dictionaries/**/dictionaries_*.pkl`

## Optional manual commands

Use these only when you need a single step:

```bash
py -3.12 scripts/dev.py clean
py -3.12 scripts/dev.py build
py -3.12 scripts/dev.py test
py -3.12 scripts/dev.py lint
```

## Optional TestPyPI upload

```bash
py -3.12 scripts/dev.py publish --repository testpypi
```

`publish` runs `check` automatically first unless you pass `--skip-check`.

## Final publish flow

```bash
py -3.12 scripts/dev.py publish
```

## Manual review items

- No generated cache files are committed.
- No `build/`, `dist/`, or `*.egg-info/` directories are committed.
- `examples/your_dictionary.dic` is not present in the built distributions.
- `scripts/` and `tests/` are absent from the built wheel.
- Optional `eng_to_ipa` behavior degrades gracefully when not installed.
- CLI works from stdin and inline text.
