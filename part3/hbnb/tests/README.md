# How to run the automated tests for this project

## Notes

- add and configure test.db
- convert all tests to unittest
- use test_client in tests

### Decisions

- chose unittest
- chose to not implement an absolute path to db in config

## Prerequisites
Ensure that the Flask application is running first

```bash
flask run
```

**unittest tests**

`unittest` is native to Python - no need to install it

Navigate to the `/test` directory

Ensure that `PYTHONPATH` is set, so that the interpreter can find `app`

Run the desired test file/s

```bash
cd part3/hbnb/tests
PYTHONPATH=.. python3 -m unittest <test_file>.py
```

**pytest tests**

Install `pytest`

Navigate to the project directory `part3/hbnb`

Run the tests using `pytest`

```bash
pip install pytest
cd part3/hbnb

# Run a single file
pytest tests/<test_file>.py

# Run all tests
pytest
```

