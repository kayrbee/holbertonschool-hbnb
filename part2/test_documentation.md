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
- `first_name` : must not be empty  
- `last_name` : must not be empty  
- `email` : must not be empty and valid format  

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
