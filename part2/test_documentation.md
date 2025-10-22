### API Testing Documentation - `hbnb` project

## Overview:

This documentation illustrates the **testing and validation** process for the API endpoints of the `hbnb` project, including:

    - Validate rules implemented
    - Manual testing using `cURL`
    - Automated unit testing with `unittest`
    - A log of test cases and results

---

## Validation Rules Implemented:

### User model:

- `first_name` : must be a string and max 50 characters
- `last_name` : must be a string and max 50 characters
- `email` : must be a string and valid format

### Place model:

- `title` : must not empty.
- `price` : must be a positive number.
- `latitude` : must be between -90 and 90.
- `longitude` : must be between -180 and 180.

### Amenities model:

- `name` : must be a string and max 25 characters

### Review model:

- `comment` : must not be empty.
- `user_id` : must reference valid user.
- `place_id` : must reference valid place.

---

## Manual testing using `cURL`:

### User entity:

Base URL: `http://127.0.0.1:5000/api/v1/users/`

**1. POST - Create a User**

```bash
curl -i -X POST "http://127.0.0.1:5000/api/v1/users/" \
-H "Content-Type: application/json" \
-d '{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com"
}'
```

**Expected status:** `201 Created`

**Expected response:**

```bash
{
    "id": "be79e2c1-be43-4af3-8228-6a2ef9c68b4d",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com"
}
```

**2. POST - Create a User (Invalid Email Format)**

```bash
curl -i -X POST "http://127.0.0.1:5000/api/v1/users/" \
-H "Content-Type: application/json" \
-d '{
  "first_name": "",
  "last_name": "",
  "email": "john.doeexample.com"
}'
```

**Expected status:** `400 Bad Request`

**Expected response:**

```bash
{
    "error": "Invalid Email. Try again"
}
```

**3. POST - Create User (Missing Required Field)**

```bash
curl -X POST "http://127.0.0.1:5000/api/v1/users/" -H "Content-Type: application/json" -d '{

  "last_name": "Doe",
  "email": "jack.doeexample.com"
}'
```

**Expected status:** `400 Bad Request`

**Expected response:**

```bash
{
    "errors": {
        "first_name": "'first_name' is a required property"
    },
    "message": "Input payload validation failed"
}
```

**4. GET - Retrieve All Existing Users**

```bash
curl -X GET "http://127.0.0.1:5000/api/v1/users/" -H "Content-Type: application/json"
```

**Expected status:** `200 OK`

**Expected response:**

```bash
{
    "id": "be79e2c1-be43-4af3-8228-6a2ef9c68b4d",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com"
}
```

**5. GET - Retrieve Existing User by ID**

```bash
curl -X GET "http://127.0.0.1:5000/api/v1/users/be79e2c1-be43-4af3-8228-6a2ef9c68b4d" -H "Content-Type: application/json"
```

**Expected status:** `200 OK`

**Expected response:**

```bash
{
    "id": "be79e2c1-be43-4af3-8228-6a2ef9c68b4d",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com"
}
```

**6. GET - Non-existent User**

```bash
curl -X GET "http://127.0.0.1:5000/api/v1/users/be79e2c1-be43-4af3-8228-6a2ef9c70v5g" -H "Content-Type: application/json"
```

**Expected status:** `404 NOT FOUND`

**Expected response:**

```bash
{
    "error": "User not found"
}
```

**7. PUT - Update a User**

```bash
curl -X PUT http://127.0.0.1:5000/api/v1/users/be79e2c1-be43-4af3-8228-6a2ef9c68b4d -H "Content-Type: application/json" -d '{
  "first_name": "Jack",
  "last_name": "Do",
  "email": "jack.do@example.com"
}'
```

**Expected status:** `200 OK`

**Expected response:**

```bash
{
    "id": "be79e2c1-be43-4af3-8228-6a2ef9c68b4d",
    "first_name": "Jack",
    "last_name": "Do",
    "email": "jack.do@example.com"
}
```

### Place entity:

Base URL: `http://127.0.0.1:5000/api/v1/places/`

**1. Create a new place (Valid Data – 201 Created)**

```bash
curl -i -X POST "http://127.0.0.1:5000/api/v1/places/" \
-H "Content-Type: application/json" \
-d '{
"title": "Cozy Apartment",
"description": "A nice place to stay",
"price": 100.0,
"latitude": 37.7749,
"longitude": -122.4194,
"owner_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
"amenities": "pool",
}'
```

Expected Response:

```bash
{
    "id": "df1fdae7-156e-4d53-b234-df05a5670b1a",
    "title": "Cozy Apartment",
    "description": "A nice place to stay",
    "price": 100.0,
    "latitude": 37.7749,
    "longitude": -122.4194,
    "owner_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "amenities": [
        "wifi",
        "pool"
    ],
    "reviews": []
}

// 201 Created
```

Possible Status Codes:

- `201 Created`: When the place is successfully created.
- `400 Bad Request`: If input data is invalid.

**2. Create with optional/empty description (201 Created)**

```bash
curl -i -X POST "http://127.0.0.1:5000/api/v1/places/" \
-H "Content-Type: application/json" \
-d '{
"title": "Beach House",
"description": "",
"price": 200,
"latitude": -37.8,
"longitude": 144.9,
"owner_id": "user123",
"amenities": ["wifi", "pool"]
}'
```

Expected Response

```bash
{
    "id": "e0f6a280-6958-4a47-acbe-e7c0505e2fbe",
    "title": "Beach House",
    "description": "",
    "price": 200,
    "latitude": -37.8,
    "longitude": 144.9,
    "owner_id": "user123",
    "amenities": [
        "wifi",
        "pool"
    ],
    "reviews": []
}

// 201 Created
```

Possible Status Codes:

- `201 Created`: When the place is successfully created.
- `400 Bad Request`: If input data is invalid.

**3. Retrieve all places**

```bash
curl -i -X GET "http://127.0.0.1:5000/api/v1/places/" \
-H "Content-Type: application/json"
```

Expected Response:

```bash
[
    {
        "id": "f6ab2715-5f14-489a-bb80-c837213709b8",
        "title": "string",
        "description": "string",
        "price": 0,
        "latitude": 0,
        "longitude": 0,
        "owner_id": "string",
        "amenities": [
            "string"
        ],
        "reviews": [
            {
                "id": "string",
                "text": "string",
                "rating": 0,
                "user_id": "string"
            }
        ]
    }
]

// 200 OK
```

**4. Retrieve Place Details by ID**

```bash
curl -i -X GET "http://127.0.0.1:5000/api/v1/places/123" \
-H "Content-Type: application/json"
```

Possible Status Codes:

- `200 OK`: When the place and its associated owner and amenities are successfully retrieved.
- `404 Not Found`: If the place does not exist.

**5. Update a Place’s Information by ID**

```bash
curl -i -X PUT "http://127.0.0.1:5000/api/v1/places/123" \
-H "Content-Type: application/json" \
-d '{
  "title": "Luxury Condo",
  "description": "An upscale place to stay",
  "price": 200.0
}'
```

Possible Status Codes:

- `200 OK`: When the place is successfully updated.
- `404 Not Found`: If the place does not exist.
- `400 Bad Request`: If input data is invalid.

**6. Missing required fields (400 Bad Request)**

```bash
curl -i -X POST "http://127.0.0.1:5000/api/v1/places/" \
-H "Content-Type: application/json" \
-d '{
"title": "",
"description": "",
"price": 200,
"latitude": -37.8,
"longitude": 144.9,
"owner_id": "user123",
"amenities": ["wifi", "pool"]
}'
```

Expected Response

```bash
{
    "error": "Title cannot be empty."
}

// 400 Bad Request
```

**7. Negative price (400 Bad Request)**

```bash
curl -i -X POST "http://127.0.0.1:5000/api/v1/places/" \
-H "Content-Type: application/json" \
-d '{
"title": "",
"description": "",
"price": -17,
"latitude": -37.8,
"longitude": 144.9,
"owner_id": "user123",
"amenities": ["wifi", "pool"]
}'
```

Expected Response

```bash
{
    "error": "Price must be a positive number"
}

// 400 Bad Request
```

**8. Invalid coordinates (400 Bad Request)**

```bash
curl -i -X POST "http://127.0.0.1:5000/api/v1/places/" \
-H "Content-Type: application/json" \
-d '{
"title": "",
"description": "",
"price": 200,
"latitude": 100,
"longitude": 144.9,
"owner_id": "user123",
"amenities": ["wifi", "pool"]
}'
```

Expected Response

```bash
{
    "error": "Latitude must be between -90 and 90"
}

// 400 Bad Request
```

### Amenities entity:

Base URL: `http://127.0.0.1:5000/api/v1/places/`

**1. POST - Create a new amenity (Valid Data – 201 Created)**

```bash
curl -X POST -H 'Content-Type: application/json' -d '{"name": "Aesop hand wash"}' http://127.0.0.1:5000/api/v1/amenities/
```

Expected Response

```bash
{
    "id": "97fad86c-2008-43c7-b6ea-dbd2b20350dd",
    "name": "Aesop hand wash"
}

// 201 Created
```

**2. GET - Retrieve amenity list (Valid Data – 200 OK)**

```bash
curl -X POST -H 'Content-Type: application/json' -d '{"name": "Aesop hand wash"}' http://127.0.0.1:5000/api/v1/amenities/
curl -X POST -H 'Content-Type: application/json' -d '{"name": "Pool"}' http://127.0.0.1:5000/api/v1/amenities/
```

```bash
curl -X GET -H 'Content-Type: application/json' http://127.0.0.1:5000/api/v1/amenities/
```

Expected Response

```bash
[
    {
        "id": "68698cec-6dee-4a7c-8c61-c95053c3e310",
        "name": "Aesop hand wash"
    },
    {
        "id": "a52d9913-5b3b-412c-bb96-d7c90d583e50",
        "name": "Pool"
    }
]

// 200 OK
```

**3. POST - Add amenity exceeding 25 characters (400 Bad Request)**

```bash
curl -X POST -H 'Content-Type: application/json' -d '{"name": "Aesop hand wash from the himalayas"}' http://127.0.0.1:5000/api/v1/amenities/
```

Expected Response

```bash
{
    "error": "Amenity length cannot exceed 25 characters"
}

// 400 Bad Request
```

### Review entity:

Prerequisites: user_id and place_id are valid

Create a review:

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d "{\"comment\": \"Great place to stay\", \"rating\": 5, \"user_id\": \"$USER\", \"place_id\": \"$PLACE\"}" \
http://127.0.0.1:5000/api/v1/reviews/
```

Update a review

```bash
curl -X PUT http://127.0.0.1:5000/api/v1/reviews/$REVIEW \
  -H "Content-Type: application/json" \
  -d '{"comment": "Updated comment", "rating": 4}'
```

List all reviews

```bash
curl http://127.0.0.1:5000/api/v1/reviews/
```

Get review by ID

```bash
curl http://127.0.0.1:5000/api/v1/reviews/$REVIEW
```

Get review by place IDgit

```bash
curl http://127.0.0.1:5000/api/v1/places/$PLACE/reviews
```

Delete a review

```bash
curl -X DELETE http://127.0.0.1:5000/api/v1/reviews/$REVIEW
```

---

## Generate Swagger Documentation

To access the Swagger documentation:

```
http://127.0.0.1:5000/api/v1/
```

---

## Automated testing using `unittest`:

All test files can be found in the [tests](tests/) directory
