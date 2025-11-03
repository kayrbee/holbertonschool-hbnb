# How to run this application

## Clean installation

### 1. Set up a Virtual Environment

```bash
cd part3/hbnb
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

This should install `flask_restx`, but if it doesn't, jump to Troubleshooting


### 2. Run application

There are two ways to launch the application. Take note of which directory you need to be in for each

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
### 3. Run tests

Jump to (test_documentation.md)[]  # add link

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