# Overview

To Do: Describe the purpose of each directory and file

## How to run this application

### Set up a Virtual Environment

```
cd part2/hbnb
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

This should install `flask_restx`, but if it doesn't, jump to Troubleshooting


### Run app

1. Change directory to application's project root

    Note that `cd` is necessary because there are additional layers of folders in the repo

    `cd holbertonschool-hbnb/part2`

2. Launch Flask app

    `hbnb/run.py`

### Troubleshooting

#### Install Dependencies

Install flask_restx

`pip install flask-restx`

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