# Part 3

## Table of Contents

- (Project structure)[] (add link)
- Setup Instructions (add link)

## Project structure

```
holbertonschool-hbnb/
├── part1/    # truncated for clarity
├── part2/    # truncated for clarity
├── part3/
│   ├──hbnb/
│   │   ├── app/
│   │   │   ├── __init__.py
│   │   │   ├── api/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── v1/
│   │   │   │       ├── __init__.py
│   │   │   │       ├── users.py
│   │   │   │       ├── places.py
│   │   │   │       ├── reviews.py
│   │   │   │       ├── amenities.py
│   │   │   ├── models/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── user.py
│   │   │   │   ├── place.py
│   │   │   │   ├── review.py
│   │   │   │   ├── amenity.py
│   │   │   ├── services/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── facade.py
│   │   │   ├── persistence/
│   │   │       ├── __init__.py
│   │   │       ├── repository.py
│   │   ├── tests/
│   │   │   ├── test_amenity.py
│   │   │   ├── test_documentation.md  # How to run the project's test suites
│   │   │   ├── test_place.py
│   │   │   ├── test_review_api.py
│   │   │   ├── test_review_class.py
│   │   │   ├── test_review_class.py
│   │   │   ├── users_test.py
│   │   ├── run.py
│   │   ├── config.py
│   │   ├── requirements.txt
│   │   ├── README.md    # How to run the application
│   ├── README.md    # You are here
├── .gitignore
├── README.md
```