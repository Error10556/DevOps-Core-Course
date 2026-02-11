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

# Task 2

## Workflow trigger strategy and reasoning

I run:
- the CI job on every push, so that we always know if the program is OK or not;
- the docker build also on every push (so that we know if it fails), but only if tests have passed;
- the docker push after every successful build, but only if this is a tagged commit (for semantic versioning).

Note that this workflow remains correct if I decide to tag a commit that is not a tip of a branch.

The downside is that if the tagged commit is the tip of the current branch, then tests and build run twice; I do not
know if there is a way to fix that.

## Action choice justification

All actions that I used (listed below) are mentioned in the lecture.

- actions/checkout@v4
- actions/setup-python@v5
- docker/login-action@v3
- docker/metadata-action@v5
- docker/build-push-action@v6

## Docker tagging strategy

I chose SemVer because we are developing a service that other applications are supposed to depend on. It will be helpful
to know when a breaking change occurs.

## Link to workflow run

This run pushed to Docker Hub:

[github.com/Error10556/DevOps-Core-Course/actions/runs/21909811285](https://github.com/Error10556/DevOps-Core-Course/actions/runs/21909811285)

## Green checkmark

All the checkmarks:

![Screenshot of a successful GitHub Actions view](/app_python/docs/screenshots/Lab3-green-checkmark.png)


