
---
**💁‍♀️ 🔗 Handy navigation links 🔗 💁‍♀️**

You are in the Application Setup Guide 🗺️

- ➡️ Jump to -------- [Test Documentation](/part4/hbnb/tests/README.md)
- ⬅️ Jump back to --- [Part 4 Project Guide](/part4/hbnb/README.md)
- ⬅️ Jump back to --- [Repository Root](/README.md)
---
# Application Setup Guide

This README details the instructions for running the Part 4 application.

## Table of Contents

- [Running the application](/part4/hbnb/README.md#Running-the-application)
  - [1. Clone the repo](/part4/hbnb/README.md#1-clone-the-repository)
  - [2. Set up a virtual environment](/part4/hbnb/README.md#2-set-up-a-virtual-environment)
  - [3. Create a .env file](/part4/hbnb/README.md#3-create-a-env-file)
  - [4. Seed the database](/part4/hbnb/README.md#4-seed-the-database)
  - [5. Run the application](/part4/hbnb/README.md#5-run-the-application)
- [Using the application](/part4/hbnb/README.md#Using-the-application)
  - [1. Optional step - validate the setup](/part4/hbnb/README.md#1-optional-step---validate-the-setup)
  - [2. Access the web front-end](/part4/hbnb/README.md#2-access-the-web-front-end)
  - [3. About the application's pages](/part4/hbnb/README.md#3-visit-application-pages)
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

### 3. Create a `.env` file

Copy [.env-example](/part4/hbnb/app/.env-example) and save it as `.env` in the same directory as the example file.

This will ensure that the app initialisation can discover the JWT_SECRET_KEY environment variable it needs.

### 4. Seed the database

A db file with empty tables already exists in this project. This step seeds the users table with an `admin_user` to enable testing the API. 

```bash
sqlite3 instance/development.db < seed.sql
```

### 5. Run the application

There are two ways to launch the application. 

**Using `run.py`**

This option is the preferred method of running the application, because it respects any config that's been passed in via `run.py`.

```bash
cd holbertonschool-hbnb/part4
python3 hbnb/run.py
```

**Using `flask run`**

This option creates an instance of a flask application, but it bypasses any config that's been passed in via `run.py`. Instead, it uses Flask's standard config options. Good as a shortcut for local testing where you don't need to worry about configuration. 

```bash
cd holbertonschool-hbnb/part4/hbnb
flask run

# Run with optional debugger
flask run --debug
```


## Using the application

### 1. Optional step - Validate the setup

Verify on the CLI that the database was seeded. You should see one admin user returned in the response, which will allow you to perform CRUD operations via the application endpoints.

```bash
curl http://127.0.0.1:5000/api/v1/users/
```

### 2. Access the web front-end

The web front-end is available at the below URL when the application:

```
http://127.0.0.1:5000/
```

**Log in as the admin**

To do - update these instructions

```
http://127.0.0.1:5000/
```
### 3. About the application's pages

To do - fill in as we go

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