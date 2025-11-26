
---
**💁‍♀️ 🔗 Handy navigation links 🔗 💁‍♀️**

You are in the Application Setup Guide ------------------ 🗺️ `/part4/hbnb`

- Jump to [Testing Guide](/part4/hbnb/tests/README.md) ----------------------------- ➡️ `/part4/hbnb/tests`
- Jump back to [Part 4 Project Guide](/part4/README.md) ----------------- ⬅️ `/part4`
- Jump back to [Repository Root](/README.md) --------------------- ⬅️ `/`
---
# Application Setup Guide

This README details the instructions for running and using the Part 4 application.

## Table of Contents

- [Running the application](/part4/hbnb/README.md#Running-the-application)
  - [1. Clone the repo](/part4/hbnb/README.md#1-clone-the-repository)
  - [2. Set up a virtual environment](/part4/hbnb/README.md#2-set-up-a-virtual-environment)
  - [3. Create a .env file](/part4/hbnb/README.md#3-optional-create-a-env-file)
  - [4. Initialise the database](/part4/hbnb/README.md#4-create--initialise-the-database)
  - [5. Seed the database](/part4/hbnb/README.md#5-seed-the-database)
  - [6. Run the application](/part4/hbnb/README.md#6-run-the-application)
- [Using the application](/part4/hbnb/README.md#Using-the-application)
  - [1. Optional step - validate the setup](/part4/hbnb/README.md#1-optional-validate-the-db-setup)
  - [2. Access the web front-end](/part4/hbnb/README.md#2-access-the-web-front-end)
  - [3. Log in as the admin](/part4/hbnb/README.md#3-log-in-as-the-admin)
- [Using the API Endpoints directly](/part4/hbnb/README.md#using-the-endpoints-directly)
  - [Swagger documentation](/part4/hbnb/README.md#1-swagger-documentation)
  - [About the endpoints](/part4/hbnb/README.md#2-about-the-endpoints)


## Running the application

### 1. Clone the repository

```bash
git clone https://github.com/kayrbee/holbertonschool-hbnb
cd holbertonschool-hbnb/part4/hbnb
```

### 2. Set up a Virtual Environment

**MacOS/Ubuntu**

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. [OPTIONAL] Create a `.env` file

Please skip to step 4

ℹ️ This step has been marked as optional because the basic instructions specified a default value for the JWT key. Our group has a stretch goal to take it a step further, which we'll work on if we've got time.


Copy [.env-example](/part4/hbnb/app/.env-example) and save it as `.env` in the same directory as the example file. To use the `.env` file, install `python-dotenv`.

```bash
pip install python-dotenv
```


### 4. Create & initialise the database

This project is backed by a sqlite database. To create and initialise a fresh database, run these setup commands from a `flask shell`:

NB: to start fresh, delete the `development.db` file first.

```bash
# Delete the old database if it exists
rm instance/development.db

# open flask shell
flask shell

# run the setup commands
>>> from app import db
>>> db.create_all()

# exit the shell
>>> exit()
```

### 5. Seed the database

The previous step created a `development.db` file. This step will seed a small set of linked data:

- the users table with an `admin_user` and some non-admin users
- the places table with places owned by non-admins
- the amenities table
- the places.amenities table with place<>amenity associations
- the reviews table with reviews of places

```bash
sqlite3 instance/development.db < seed.sql
```

#### 5a. [OPTIONAL] If `sqlite3` is not installed

**MacOS Homebrew**
```bash
brew install sqlite
sqlite3 --version

# Then try step 5 again
```

**Ubuntu**
```bash
sudo apt update
sudo apt install sqlite3
sqlite3 --version

# Then try step 5 again
```

**Windows**

- Download the SQLite tools ZIP from:
https://www.sqlite.org/download.html

(Look for "sqlite-tools")
- Unzip it somewhere (e.g. C:\sqlite)
- Add that folder to your PATH:
  - Start → “Edit environment variables”
  - Edit PATH → Add C:\sqlite

```bash
sqlite3 --version

# Then try step 5 again
```

### 6. Run the application

There are two ways to launch the application. 

**Using `run.py`**

This option is the preferred method of running the application, because it respects any config that's been passed in via `run.py`.

```bash
# Check your location
cd holbertonschool-hbnb/part4/hbnb

# Start the application
python3 run.py
```

**Using `flask run`**

This option creates an instance of a flask application, but it bypasses any config that's been passed in via `run.py`. Instead, it uses Flask's standard config options. Good as a shortcut for local testing where you don't need to worry about handling multiple configurations. 

```bash
cd holbertonschool-hbnb/part4/hbnb
flask run

# Run with optional debugger
flask run --debug
```


## Using the application

### 1. [OPTIONAL] Validate the db setup

You can verify that the database was seeded correctly if you want to. You should see one admin user returned in the response, which will allow you to perform CRUD operations via the application endpoints.

```bash
curl http://127.0.0.1:5000/api/v1/users/
```

### 2. Access the web front-end

The web front-end is available on port 5000 while the application is running:

```
http://127.0.0.1:5000
```

The web pages are
- [Home](http://127.0.0.1:5000)
- [Login](http://127.0.0.1:5000/login)
- [Place](http://127.0.0.1:5000/place)
- [Review]() # add link when done

### 3. Log in as the admin**

Visit the login page and sign in as the admin

```bash
http://127.0.0.1:5000/login

email: # admin email
password: # admin password (see intranet)
```

## Using the API endpoints directly

The following information has been copied across from Part 3. The endpoints are still available for direct interaction without the front-end, so we've included the instructions for completeness.

### 1. Swagger documentation

The Swagger API will be available at:

```bash
http://127.0.0.1:5000/api/v1/
```

### 2. About the endpoints

Login as the admin. The password is available on the intranet - make sure to replace it in the below command before executing it. It should return a valid jwt token. 

```bash
curl -X POST "http://127.0.0.1:5000/api/v1/auth/login" \
-H "Content-Type: application/json" \
-d '{
  "email": "admin@hbnb.io",
  "password": "{password}"
}' 
```

**Users**

```bash
GET /api/v1/users/              # Get all users
GET /api/v1/users/{user_id}     # Get user by user_id
PUT /api/v1/users/{user_id}     # Update user details except email and password
```

**Auth**

```bash
POST /api/v1/auth/login        # Login with email and password
```

**Admin**

```bash
POST /api/v1/users/            # Admin can create new users
PUT /api/v1/users/{user_id}    # Admin can update user information
DELETE /api/v1/users/{user_id} # Admin can delete users
POST /api/v1/amenities/        # Admin can create amenities
PUT /api/v1/amenities/{amenity_id} # Admin can update amenity
DELETE /api/v1/amenities/{amenity_id} # Admin can delete amenity
PUT /api/v1/reviews/{review_id} # Admin can update reviews
DELETE /api/v1/reviews/{amenity_id} # Admin can delete reviews
PUT /api/v1/places/{place_id}  # Admin can update places
DELETE /api/v1/places/{place_id} # Admin can delete places
```

**Places**

```bash
GET /api/v1/places/            # Get all places
GET /api/v1/places/{place_id}  # Get place details
POST /api/v1/places/           # Create a new place
PUT /api/v1/places/{place_id}  # Update place information
DELETE /api/v1/places/{place_id} # Delete a place
```

**Reviews**

```bash
GET /api/v1/reviews/            # Get all reviews
GET /api/v1/reviews/{review_id}  # Get reviews details
GET /api/v1/places/{place_id}/reviews # Get all reviews of a place by place_id
POST /api/v1/reviews/           # Create a new review
PUT /api/v1/reviews/{review_id}  # Update review information
DELETE /api/v1/reviews/{review_id} # Delete a review
```

**Amenities**

Most amenity actions are admin-only - see Admin endpoints

```bash
GET /api/v1/amenities/         # Get all amenities
GET /api/v1/amenities/{amenity_id}  # Get amenity details
```

## More CURL examples

[curl examples](/part4/hbnb/tests/curl_tests.md)

## Automated testing (test coverage includes all CRUD operations)

[Running the automated testing for API and class entities](/part4/hbnb/tests/README.md)