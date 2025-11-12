# How to run this application

## Running the tests


For information on how to run the automated test suites, jump to [test documentation](/part3/hbnb/tests/README.md)

## Running the application

### 1. Clone the repository

```bash
git clone https://github.com/kayrbee/holbertonschool-hbnb
cd holbertonschool-hbnb/part3/hbnb
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

Copy [.env-example](/part3/hbnb/app/.env-example) and save it as `.env` in the same directory as the example file.

This will ensure that the app initialisation can discover the JWT_SECRET_KEY environment variable it needs.

### 5. Seed the database

A db file with empty tables already exists in this project. This step seeds the users table with an `admin_user` to enable testing the API. 

```bash
sqlite3 instance/development.db < seed.sql
```

### 6. Run application

There are two ways to launch the application. 

**Using `flask run`**

This is the preferred method because (I think) there's a bug in `run.py` we haven't fixed yet

```bash
cd holbertonschool-hbnb/part3/hbnb
flask run

# Run with optional debugger
flask run --debug
```

**Using `run.py`**

```bash
cd holbertonschool-hbnb/part3
python3 -m hbnb/run.py
```


### Using the application

### Validate the setup

Verify on the CLI that the database was seeded. You should see one admin user returned in the response, which will allow you to perform CRUD operations via the application endpoints.

```bash
curl http://127.0.0.1:5000/api/v1/users/
```

Login as the admin. The password is available on the intranet - make sure to replace it in the below command before executing it. It should return a valid jwt token. 

```bash
curl -X POST "http://127.0.0.1:5000/api/v1/auth/login" \
-H "Content-Type: application/json" \
-d '{
  "email": "admin@hbnb.io",
  "password": "{password}"
}' 
```

### Swagger documentation

The Swagger API will be available at:

```bash
http://127.0.0.1:5000/api/v1/
```

### Endpoints

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

[curl examples](/part3/hbnb/tests/curl_tests.md)

## Automated testing (test coverage includes all CRUD operations)

[Running the automated testing for API and class entities](/part3/hbnb/tests/README.md)