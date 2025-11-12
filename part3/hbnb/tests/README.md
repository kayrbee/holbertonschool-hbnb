# How to run the automated tests for this project


**unittest tests**

`unittest` is native to Python - no need to install it. Before running the tests, make sure you're in a `venv` environment (see [set up a virtual environment](/part3/hbnb/README.md)). 

To run the automated tests:
```bash
cd part3/hbnb

# Run individual file by file_name
python3 -m unittest tests/<file_name>.py

# Run all tests
python3 -m unittest
```

**curl tests**

For guidance on how to run curl tests, see [curl tests](/part3/hbnb/tests/curl_tests.md)

## Kat's WIP Test Notes

### General Objective of the Test Refactor

- convert all tests to `unittest` framework
- remove `pytest`
- use test_client config in tests to avoid filling development.db with junk data
- improve coverage in all test files

### Decision Record

- chose `unittest` over `pytest`
- chose to not implement an absolute path to db in config (yet)
- chose to configure a test db that runs in-memory (avoids need for tearDown() method)
- chose to isolate class tests from the db because the db is included in the api tests

### Done

MVP definition of done: 
- test file uses `unittest`, 
- tests in the file use a test db (api tests) or are isolated from the db (class tests), and 
- all tests in the file passed when run from the CLI

Extension: make sure every test file covers all CRUD operations and defined error paths

- add and configure test.db
- test_auth_api.py
- test_amenity_api.py
- test_amenity_class.py
- test_place_class.py
- test_review_class.py
- test_review_api.py
- test_user_class.py
- test_user_api.py

### To do

- test_place_api.py [in progress - waiting on Mel]
- Debugging of known issues on admin
