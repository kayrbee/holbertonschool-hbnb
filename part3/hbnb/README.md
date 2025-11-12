# How to run this application

### 1. Set up a Virtual Environment

```bash
cd part3/hbnb
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

This should install `flask_restx` and `bcrypt`, but if it doesn't, jump to Troubleshooting

### 2. Create a `.env` file

Copy [.env-example](part3/hbnb/app/.env-example) and save it as `.env` in the same directory as the example file.

This will ensure that the app initialisation can discover the JWT_SECRET_KEY environment variable it needs.


### 3. Run application

There are two ways to launch the application. Take note of which directory you need to be in for each method.

**Using run.py file**

```bash
cd holbertonschool-hbnb/part3
python3 -m hbnb/run.py
```
**Using `flask run` command**

```bash
cd holbertonschool-hbnb/part3/hbnb
flask run

# Run with optional debugger
flask run --debug
```
### 4. Run tests

Jump to [test_documentation.md](/part3/hbnb/tests/test_documentation.md)

### Troubleshooting

#### Module Not Found
If Python complains of `ModuleNotFound` errors, try setting the PYTHONPATH

    Example: `PYTHONPATH=hbnb python3 hbnb/app/models/test-review.py`

If that works, the temporary fix is: `export PYTHONPATH=hbnb`

The permanent/runtime fix is currently untested, but something like this should work:
```
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))  # adds hbnb/
```

test 
test
test