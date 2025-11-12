# API Testing Documentation

## Table of Contents
1. [User Management Tests](#user-management-tests)
2. [Amenity Management Tests](#amenity-management-tests)
3. [Place Management Tests](#place-management-tests)
4. [Review Management Tests](#review-management-tests)
5. [Test Summary](#test-summary)

---

## User Management Tests

### Test 1: Create Admin User
**Purpose:** Create an admin user with elevated privileges

**Request:**
```bash
POST /api/v1/users/debug-create
Content-Type: application/json

{
  "email": "admin5@example.com",
  "first_name": "Admin",
  "last_name": "User5",
  "password": "securepassword123",
  "is_admin": true
}
```

**Response:**
```json
{
  "id": "e9c83c77-8cb7-437b-8bb8-24c5c6df34fa",
  "message": "User registered successfully"
}
```

**Result:** ✅ Pass

---

### Test 2: Admin Login
**Purpose:** Authenticate admin user and receive access token

**Request:**
```bash
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "admin5@example.com",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Result:** ✅ Pass  
**Note:** Token contains `"is_admin": true` in JWT payload

---

### Test 3: Register Second User
**Purpose:** Create a standard (non-admin) user

**Request:**
```bash
POST /api/v1/users/
Authorization: Bearer {admin_token}
Content-Type: application/json

{
  "email": "user2@example.com",
  "first_name": "Second",
  "last_name": "User",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "id": "f0edfaf9-0fab-4bbf-9ace-01c29b9f82eb",
  "message": "User registered successfully"
}
```

**Result:** ✅ Pass

---

### Test 4: Second User Login
**Purpose:** Authenticate standard user

**Request:**
```bash
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "user2@example.com",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Result:** ✅ Pass  
**Note:** Token contains `"is_admin": false` in JWT payload

---

### Test 5: Register Third User
**Purpose:** Create another standard user for authorization testing

**Request:**
```bash
POST /api/v1/users/
Authorization: Bearer {admin_token}
Content-Type: application/json

{
  "email": "NOTADMIN@example.com",
  "first_name": "Third",
  "last_name": "User",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "id": "940f8e92-16f9-4b4d-b5ad-97ee2ae32b84",
  "message": "User registered successfully"
}
```

**Result:** ✅ Pass

---

### Test 6: Third User Login
**Purpose:** Authenticate third user for cross-user authorization tests

**Request:**
```bash
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "NOTADMIN@example.com",
  "password": "securepassword123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Result:** ✅ Pass

---

## Amenity Management Tests

### Test 7: Create "Cellar Door" Amenity
**Purpose:** Create first amenity for place associations

**Request:**
```bash
POST /api/v1/amenities/
Authorization: Bearer {admin_token}
Content-Type: application/json

{
  "name": "Cellar Door"
}
```

**Response:**
```json
{
  "id": "62caa8d8-b830-4e33-bac9-866617a692d5",
  "name": "Cellar Door"
}
```

**Result:** ✅ Pass

---

### Test 8: Create "Wine Cellar" Amenity
**Purpose:** Create second amenity for multi-amenity testing

**Request:**
```bash
POST /api/v1/amenities/
Authorization: Bearer {admin_token}
Content-Type: application/json

{
  "name": "Wine Cellar"
}
```

**Response:**
```json
{
  "id": "f695aec9-0825-4393-8a0c-392811155c91",
  "name": "Wine Cellar"
}
```

**Result:** ✅ Pass

---

## Place Management Tests

### Test 9: Create Place Without Amenities
**Purpose:** Verify place creation with empty amenities array

**Request:**
```bash
POST /api/v1/places/
Authorization: Bearer {admin_token}
Content-Type: application/json

{
  "title": "Wine Country",
  "description": "All you can wine",
  "price": 5000.0,
  "latitude": -7.8136,
  "longitude": 14.9631,
  "owner_id": "52c448d4-9b1d-4186-ab35-bb9276da9cfb"
}
```

**Response:**
```json
{
  "id": "552713cb-488f-4443-ba4e-98630489165a",
  "title": "Wine Country",
  "description": "All you can wine",
  "price": 5000.0,
  "latitude": -7.8136,
  "longitude": 14.9631,
  "owner_id": "52c448d4-9b1d-4186-ab35-bb9276da9cfb",
  "amenities": [],
  "reviews": []
}
```

**Result:** ✅ Pass

---

### Test 10: Create Place With Single Amenity
**Purpose:** Test amenity association with places

**Request:**
```bash
POST /api/v1/places/
Authorization: Bearer {admin_token}
Content-Type: application/json

{
  "title": "Bat Country",
  "description": "All you can bat",
  "price": 5000.0,
  "latitude": -7.8136,
  "longitude": 14.9631,
  "owner_id": "e9c83c77-8cb7-437b-8bb8-24c5c6df34fa",
  "amenities": ["62caa8d8-b830-4e33-bac9-866617a692d5"]
}
```

**Response:**
```json
{
  "id": "71e0843e-fbc4-421d-b780-ab6f9b2c1e61",
  "title": "Bat Country",
  "description": "All you can bat",
  "price": 5000.0,
  "latitude": -7.8136,
  "longitude": 14.9631,
  "owner_id": "e9c83c77-8cb7-437b-8bb8-24c5c6df34fa",
  "amenities": [
    {
      "id": "62caa8d8-b830-4e33-bac9-866617a692d5",
      "name": "Cellar Door"
    }
  ],
  "reviews": []
}
```

**Result:** ✅ Pass

---

### Test 11: Create Place With Multiple Amenities
**Purpose:** Test multiple amenity associations

**Request:**
```bash
POST /api/v1/places/
Authorization: Bearer {admin_token}
Content-Type: application/json

{
  "title": "Juice Country",
  "description": "All you can squeeze",
  "price": 5000.0,
  "latitude": -7.8136,
  "longitude": 14.9631,
  "owner_id": "52c448d4-9b1d-4186-ab35-bb9276da9cfb",
  "amenities": [
    "f85aa03c-7369-4c40-b80e-ef6070787d12",
    "10c4f8b9-7e14-43af-8493-f84eca66dd3f"
  ]
}
```

**Response:**
```json
{
  "id": "eee7f910-9fcf-44ab-a1fb-36cb7e351902",
  "title": "Juice Country",
  "description": "All you can squeeze",
  "price": 5000.0,
  "latitude": -7.8136,
  "longitude": 14.9631,
  "owner_id": "52c448d4-9b1d-4186-ab35-bb9276da9cfb",
  "amenities": [
    {
      "id": "10c4f8b9-7e14-43af-8493-f84eca66dd3f",
      "name": "Cellar Door"
    },
    {
      "id": "f85aa03c-7369-4c40-b80e-ef6070787d12",
      "name": "Wine Cellar"
    }
  ],
  "reviews": []
}
```

**Result:** ✅ Pass

---

### Test 12: Update Place As Owner
**Purpose:** Verify owner can update their own place and modify amenities

**Request:**
```bash
PUT /api/v1/places/eee7f910-9fcf-44ab-a1fb-36cb7e351902
Authorization: Bearer {owner_token}
Content-Type: application/json

{
  "title": "Updated Juice Country",
  "description": "Now with extra pulp",
  "price": 5200.0,
  "latitude": -7.8136,
  "longitude": 14.9631,
  "owner_id": "52c448d4-9b1d-4186-ab35-bb9276da9cfb",
  "amenities": ["f85aa03c-7369-4c40-b80e-ef6070787d12"]
}
```

**Response:**
```json
{
  "id": "eee7f910-9fcf-44ab-a1fb-36cb7e351902",
  "title": "Updated Juice Country",
  "description": "Now with extra pulp",
  "price": 5200.0,
  "latitude": -7.8136,
  "longitude": 14.9631,
  "owner_id": "52c448d4-9b1d-4186-ab35-bb9276da9cfb",
  "amenities": [
    {
      "id": "f85aa03c-7369-4c40-b80e-ef6070787d12",
      "name": "Wine Cellar"
    }
  ],
  "reviews": [],
  "owner": {
    "id": "52c448d4-9b1d-4186-ab35-bb9276da9cfb",
    "first_name": "Admin",
    "last_name": "User5",
    "email": "admin5@example.com",
    "is_admin": true
  }
}
```

**Result:** ✅ Pass  
**Note:** Amenities were successfully updated from 2 to 1

---

## Review Management Tests

### Test 13: Attempt to Review Own Property (Negative Test)
**Purpose:** Verify business logic prevents owners from reviewing their own places

**Request:**
```bash
POST /api/v1/reviews/
Authorization: Bearer {owner_token}
Content-Type: application/json

{
  "place": "2d7aa375-4369-4f49-8414-1a9f0e0f0a4c",
  "user": "52c448d4-9b1d-4186-ab35-bb9276da9cfb",
  "text": "The bats were delicious",
  "rating": 5
}
```

**Response:**
```json
{
  "error": "You cannot review your own place"
}
```

**Result:** ✅ Pass (Correctly rejected)  
**Validation:** Business logic working as expected

---

### Test 14: Create Review As User
**Purpose:** Create a valid review from a non-owner user

**Request:**
```bash
POST /api/v1/reviews/
Authorization: Bearer {user2_token}
Content-Type: application/json

{
  "place": "71e0843e-fbc4-421d-b780-ab6f9b2c1e61",
  "user": "f0edfaf9-0fab-4bbf-9ace-01c29b9f82eb",
  "text": "The wine was excellent",
  "rating": 5
}
```

**Response:**
```json
{
  "id": "21a333d0-6018-47a8-92f5-b6dc54208522",
  "rating": 5,
  "text": "The wine was excellent",
  "user": "f0edfaf9-0fab-4bbf-9ace-01c29b9f82eb",
  "place": "71e0843e-fbc4-421d-b780-ab6f9b2c1e61"
}
```

**Result:** ✅ Pass

---

### Test 15: Update Review As Author
**Purpose:** Verify review author can modify their own review

**Request:**
```bash
PUT /api/v1/reviews/6f116a2f-4481-48bd-a556-7470ca31ceaa
Authorization: Bearer {user2_token}
Content-Type: application/json

{
  "text": "The wine could've been better",
  "rating": 2
}
```

**Response:**
```json
{
  "id": "6f116a2f-4481-48bd-a556-7470ca31ceaa",
  "rating": 2,
  "text": "The wine could've been better",
  "user": "f0edfaf9-0fab-4bbf-9ace-01c29b9f82eb",
  "place": "71e0843e-fbc4-421d-b780-ab6f9b2c1e61"
}
```

**Result:** ✅ Pass

---

### Test 16: Update Review As Admin
**Purpose:** Verify admin can modify any review (elevated privileges)

**Request:**
```bash
PUT /api/v1/reviews/6f116a2f-4481-48bd-a556-7470ca31ceaa
Authorization: Bearer {admin_token}
Content-Type: application/json

{
  "text": "Cheers!",
  "rating": 5
}
```

**Response:**
```json
{
  "id": "6f116a2f-4481-48bd-a556-7470ca31ceaa",
  "rating": 5,
  "text": "Cheers!",
  "user": "f0edfaf9-0fab-4bbf-9ace-01c29b9f82eb",
  "place": "71e0843e-fbc4-421d-b780-ab6f9b2c1e61"
}
```

**Result:** ✅ Pass  
**Note:** Admin successfully modified another user's review

---

### Test 17: Update Review As Third Party (Negative Test)
**Purpose:** Verify unauthorized users cannot modify others' reviews

**Request:**
```bash
PUT /api/v1/reviews/21a333d0-6018-47a8-92f5-b6dc54208522
Authorization: Bearer {user3_token}
Content-Type: application/json

{
  "text": "Cheers!",
  "rating": 5
}
```

**Response:**
```json
{
  "error": "Unauthorized action"
}
```

**Result:** ✅ Pass (Correctly rejected)  
**Validation:** Authorization logic working correctly

---

### Test 18: Delete Review As Admin
**Purpose:** Verify admin can delete any review

**Request:**
```bash
DELETE /api/v1/reviews/6f116a2f-4481-48bd-a556-7470ca31ceaa
Authorization: Bearer {admin_token}
```

**Response:**
```json
{
  "success": "Review deleted"
}
```

**Result:** ✅ Pass

---

## Test Summary

### Overall Results
- **Total Tests:** 18
- **Passed:** 18
- **Failed:** 0
- **Success Rate:** 100%

### Test Breakdown by Category
| Category | Tests | Passed | Failed |
|----------|-------|--------|--------|
| User Management | 6 | 6 | 0 |
| Amenity Management | 2 | 2 | 0 |
| Place Management | 4 | 4 | 0 |
| Review Management | 6 | 6 | 0 |

### Key Validations Verified
✅ **Authentication & Authorization**
- JWT token generation working correctly
- Admin vs. user roles properly distinguished
- Token-based authorization enforced

✅ **Business Logic**
- Users cannot review their own properties
- Review ownership validation working
- Cross-user authorization properly blocked

✅ **Data Relationships**
- Amenity associations with places functional
- Single and multiple amenity support working
- Place-review relationships maintained

✅ **CRUD Operations**
- All create, read, update operations successful
- Delete operations working for authorized users
- Proper error responses for invalid operations

✅ **Role-Based Access Control**
- Admin can modify any resource
- Users can only modify their own resources
- Unauthorized access properly rejected