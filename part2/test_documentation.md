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




### Review model:

---

## Manual testing using `cURL`:

### User entity:
Base URL: `http://127.0.0.1:5000/api/v1/users/`

**1. POST - Create a User (Valid Data – 201 Created)**
```bash
curl -i -X POST "http://127.0.0.1:5000/api/v1/places/" \
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
curl -i -X POST "http://127.0.0.1:5000/api/v1/places/" \
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

Expected Response  
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

**3. Missing required fields (400 Bad Request)**
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

**4. Negative price (400 Bad Request)**
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

**5. Invalid coordinates (400 Bad Request)**
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


### Review entity:

---

## Generate Swagger Documentation

To access the Swagger documentation:

```
http://127.0.0.1:5000/api/v1/
```

---

## Automated testing using `unittest`:
