# Part 4 Project Guide

This README details the application's structure and the task instructions for part 4.

## Table of Contents

- [Part 4 Project Structure](/part4/README.md#part-4-app-structure)
- [Part 4 Task Overview](/part4/README.md#Part-4-Task-Overview)

**Handy links**
- ➡️ Jump to [Application Setup Guide](/part4/hbnb/README.md)
- ➡️ Jump to [Test Documentation](/part4/hbnb/tests/README.md)
- ⬅️ Jump back to [Repository Root](/README.md)


## Part 4 Project Structure

```
holbertonschool-hbnb/
├── .github/  # GitHub Actions config to run automated tests
├── part1/    # truncated for clarity
├── part2/    # truncated for clarity
├── part3/
│   ├──hbnb/
│   │   ├── app/
│   │   │   ├── api/
│   │   │   │   ├── v1/
│   │   │   │       ├── __init__.py
│   │   │   │       ├── admin.py
│   │   │   │       ├── amenities.py
│   │   │   │       ├── auth.py
│   │   │   │       ├── places.py
│   │   │   │       ├── reviews.py
│   │   │   │       ├── users.py
│   │   │   │   ├── __init__.py
│   │   │   ├── models/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── amenity.py
│   │   │   │   ├── base_class.py
│   │   │   │   ├── place.py
│   │   │   │   ├── review.py
│   │   │   │   ├── user.py
│   │   │   ├── persistence/
│   │   │   │   ├── sql/
│   │   │   │       ├── amenity_table.sql
│   │   │   │       ├── development.db
│   │   │   │       ├── insert_admin_user.sql
│   │   │   │       ├── insert_initial_amenities.sql
│   │   │   │       ├── place_amenity_table.sql
│   │   │   │       ├── place_table.sql
│   │   │   │       ├── review_table.sql
│   │   │   │       ├── user_table.sql
│   │   │   │   ├── __init__.py
│   │   │   │   ├── repository.py
│   │   │   ├── services/
│   │   │   │   ├── repositories/
│   │   │   │       ├── amenity_repository.py
│   │   │   │       ├── place_repository.py
│   │   │   │       ├── review_repository.py
│   │   │   │       ├── user_repository.py
│   │   │   │   ├── __init__.py
│   │   │   │   ├── facade.py
│   │   │   ├── __init__.py                     # Contains def create_app()
│   │   ├── images/                             # Mermaid diagrams
│   │   │   ├── Base.png
│   │   │   ├── Test_understanding.png
│   │   ├── instance/
│   │   │   ├── development.db
│   │   ├── tests/
│   │   │   ├── __init__.py
│   │   │   ├── curl_tests.md
│   │   │   ├── helper_methods.py
│   │   │   ├── README.md                        # How to run the project's test suites
│   │   │   ├── test_amenity_api.py
│   │   │   ├── test_amenity_class.py
│   │   │   ├── test_auth_api.py     
│   │   │   ├── test_place_api.py
│   │   │   ├── test_place_class.py
│   │   │   ├── test_review_api.py
│   │   │   ├── test_review_class.py
│   │   │   ├── test_user_api.py
│   │   │   ├── test_user_class.py
│   │   ├── .env-example
│   │   ├── config.py
│   │   ├── README.md                        # How to run the application
│   │   ├── requirements.txt
│   │   ├── run.py
│   ├── README.md                            # You are here
├── .gitignore
├── README.md
```

## Part 4 – Simple Web Client

In this phase, you’ll be focusing on the front-end development of your application using **HTML5**, **CSS3**, and **JavaScript ES6**. Your task is to design and implement an interactive user interface that connects with the back-end services you developed in previous parts of the project.

---

### Objectives

- Develop a user-friendly interface following provided design specifications.
- Implement client-side functionality to interact with the back-end API.
- Ensure secure and efficient data handling using JavaScript.
- Apply modern web development practices to create a dynamic web application.

---

### Learning Goals

- Understand and apply HTML5, CSS3, and JavaScript ES6 in a real-world project.
- Learn to interact with back-end services using AJAX/Fetch API.
- Implement authentication mechanisms and manage user sessions.
- Use client-side scripting to enhance user experience without page reloads.

---

### Tasks Breakdown

#### **Design (Task 1)**

- Complete provided HTML and CSS files to match the given design specifications.
- Create pages for **Login**, **List of Places**, **Place Details**, and **Add Review**.

#### **Login (Task 2)**

- Implement login functionality using the back-end API.
- Store the **JWT token** returned by the API in a cookie for session management.

#### **List of Places (Task 3)**

- Implement the main page to display a list of all places.
- Fetch places data from the API and implement client-side filtering based on country selection.
- Ensure the page redirects to the login page if the user is not authenticated.

#### **Place Details (Task 4)**

- Implement the detailed view of a place.
- Fetch place details from the API using the place ID.
- Provide access to the *Add Review* form if the user is authenticated.

#### **Add Review (Task 5)**

- Implement the form to add a review for a place.
- Ensure the form is accessible only to authenticated users, redirecting others to the index page.

---

### Notes

When testing your client against your API, you’ll probably encounter a **Cross-Origin Resource Sharing (CORS)** error.  
You’ll need to modify your API code to allow your client to fetch data from it.

For a deeper understanding of CORS and how to configure your Flask API, refer to external resources such as tutorials and documentation.

---

### Resources

[HTML5 Documentation]()  # add link  
[CSS3 Documentation]()  # add link  
[JavaScript ES6 Features]()  # add link  
[Fetch API]()  # add link  
[Responsive Web Design Basics]()  # add link  
[Handling Cookies in JavaScript]()  # add link  
[Client-Side Form Validation]()  # add link