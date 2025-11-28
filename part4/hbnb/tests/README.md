
---
**💁‍♀️ 🔗 Handy navigation links 🔗 💁‍♀️**

You are in the Testing Guide ---------------------------- 🗺️ `/part4/hbnb/tests`

- Jump back to [Application Setup Guide](/part4/hbnb/README.md) ------------- ⬅️ `/part4/hbnb`
- Jump back to [Part 4 Project Guide](/part4/README.md) ----------------- ⬅️ `/part4 `
- Jump back to [Repository Root](/README.md) --------------------- ⬅️ `/`
---

# Testing Guide

This README details information about the application's testing. 

We have configured Github Actions to automatically run our unit and API tests on every merge to master. The results of each test run are available via the GitHub UI > Actions.

## Table of Contents

- [Test approach](/part4/hbnb/tests/README.md#unittest-tests)
    - [Run all tests in part 4](/part4/hbnb/tests/README.md#run-all-tests-in-part-4)
    - [Unit tests](/part4/hbnb/tests/README.md#)
        - [Run all unit tests](/part4/hbnb/tests/README.md#run-all-unit-tests)
    - [API tests](/part4/hbnb/tests/README.md#run-all-api-tests)
    - [Testing manually with curl](/part4/hbnb/tests/README.md#testing-manually-with-curl)
    - [W3C Validation](/part4/hbnb/tests/README.md#w3c-validation)

## Test approach

Our automated tests are written with the `unittest` framework. We created test coverage of the class models and the API endpoints (using unit tests and api tests, respectively). There's no need to have the application running before running the tests, but it is necessary to be in a [virtual environment](/part4/hbnb/README.md#2-set-up-a-virtual-environment), otherwise `unittest` will throw ImportModule errors. 

> ℹ️ `unittest` is native to Python - no need to install it.


### Run all tests in part 4

```bash
# Ensure that you're in the correct directory
cd part4/hbnb

# Ensure that you're in a virtual env
source venv/bin/activate

# Run all of the tests in the part 4 project
python3 -m unittest
```


### Unit tests
The unit tests are in `/tests/models`, and are written to test each class model in isolation from both class dependencies and the database. They protect against breaking changes to the class models that the application depends on. 

#### Run all unit tests

```bash
# Ensure that you're in the correct directory
cd part4/hbnb

# Run an individual unit test file by file_name
python3 -m unittest tests/models/<file_name>.py

# Run all of the unit tests
python -m unittest discover -s tests/models
```

### API tests

The API tests are in `/tests/api`, and are written to test the CRUD behaviour of each endpoint. The API test boundary includes the database, using a SQLite test database that runs in-memory. They protect against breaking changes within the API, business logic and database layers.

We've also defined some helper functions to support the API tests in `/tests/api/helper_methods.py`.

#### Run all API tests

```bash
# Ensure that you're in the correct directory
cd part4/hbnb

# Run an individual api test file by file_name
python3 -m unittest tests/api/<file_name>.py

# Run all of the api tests
python -m unittest discover -s tests/api
```

### Testing manually with CURL

For guidance on how to test individual endpoints with curl commands, see [curl tests](/part4/hbnb/tests/curl_tests.md)

### W3C Validation

A key component of the testing for Part 4 was ensuring W3C Validation. Accordingly, final copies of the html have been tested against the [W3C Validator](https://validator.w3.org/) using rendered html code that we generated using python scripts. The following resources will assist the user with various stages of testing or test-review.
- [Rendered HTML Pages](/part4/hbnb/tests/rendered_html_pages): Contains rendered copies of the HTML as it was upon submission
- [Rendering Tools](/part4/hbnb/tests/rendered_html_pages/rendering_tools): Contains copies of the .py files used to generate the rendered HTML files. Can be re-used as needed.
- [W3C Results](/part4/hbnb/tests/rendered_html_pages/W3C_results): Contains copies of the passing results generated upon testing for W3C compliance. This is based on the rendered HTML pages provided.
