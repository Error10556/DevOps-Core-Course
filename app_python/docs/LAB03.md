# Task 1

## Testing framework

I chose `pytest` for its simplicity.

## Test structure

I created 3 files in the `tests` directory: (omitting `__init__.py`)

```text
tests
├── test_404.py     # for handling disallowed URLs
├── test_health.py  # for the /health endpoint
└── test_index.py   # for the / endpoint
```

Each of these files contains functions that use `assert`s to test the app with `app.test_client()`.

## How to test locally

1. Install and activate a virtual environment with all dependencies in `requirements-dev.txt` and `requirements.txt`:
```sh
python -m venv venv
. venv/bin/activate
pip install -r requirements-dev.txt -r requirements.txt
```
2. Run `pytest` in the `app_python` directory while having the virtual environment active:
```sh
pytest
```

## Passing tests output

```text
============================= test session starts ==============================
platform linux -- Python 3.14.2, pytest-9.0.0, pluggy-1.6.0
rootdir: /home/timur/proj/DevOps-Core-Course/app_python
collected 3 items

tests/test_404.py .                                                      [ 33%]
tests/test_health.py .                                                   [ 66%]
tests/test_index.py .                                                    [100%]

============================== 3 passed in 0.16s ===============================
```
