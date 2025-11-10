# How to run the automated tests for this project

## Notes

- convert all tests to `unittest` framework
- use test_client in tests
- improve coverage in all test files

### Decisions

- chose unittest
- chose to not implement an absolute path to db in config (yet)
- chose to configure test.db to run in-memory (avoids need for tearDown() method)

### Done

MVP definition of done: test file uses `unittest`, tests in the file use a test db, and all tests in the file passed when run from the CLI

Extension: make sure every test file covers all CRUD operations and defined error paths

- add and configure test.db
- test_auth_api.py
- test_amenity_api.py

### To do

- test_amenity_class.py
- test_place_api.py
- test_place_class.py
- test_review_api.py
- test_review_class.py
- test_user_api.py
- test_user_class.py

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

