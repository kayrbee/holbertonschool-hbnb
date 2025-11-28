
---
**💁‍♀️ 🔗 Handy navigation links 🔗 💁‍♀️**

You are in the Part 4 Project Guide  ---------------------- 🗺️ `/part4`

- Jump to [Application Setup Guide](/part4/hbnb/README.md) ------------------- ➡️ `/part4/hbnb`
- Jump to [Testing Guide](/part4/hbnb/tests/README.md) ------------------------------ ➡️  `/part4/hbnb/tests`
- Jump back to [Repository Root](/README.md) ---------------------- ⬅️ `/`
---

# Part 4 Project Guide

This README details the application's structure and the task instructions for hbnb part 4: Implementing a web front-end.

## Table of Contents

- [Part 4 Project Structure](/part4/README.md#part-4-app-structure)
- [Part 4 Task Overview](/part4/README.md#Part-4-Task-Overview)
    - [Build a simple web client](/part4/README.md#build-a-simple-web-client)
        - [Objectives](/part4/README.md#objectives)
        - [Learning goals](/part4/README.md#learning-goals)
    - [Task breakdown](/part4/README.md#tasks-breakdown)
        - [1. Design](/part4/README.md#design-task-1)
        - [2. Login](/part4/README.md#login-task-2)
        - [3. List of places](/part4/README.md#list-of-places-task-3)
        - [4. Place details](/part4/README.md#place-details-task-4)
        - [5. Add review](/part4/README.md#add-review-task-5)
    - [W3C Validation](/part4/README.md#w3c-validation)


## Part 4 Project Structure

For an overview of the project please refer to the directory structure below. Most of the structure was cloned from Part 3; Part 4 extends the structure to include a web front-end, including html, javascript, css and image files. 

We've also uploaded a copy of the fully rendered html of each page, to assist the marking process - they're not required for the application to function.

```
holbertonschool-hbnb/
├── .github/                        # GitHub Actions config to run automated tests
├── part1/                          # truncated for clarity
├── part2/                          # truncated for clarity
├── part3/                          # truncated for clarity
├── part4/
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
│   │   │   ├── static/
│   │   │   │   ├── css/
│   │   │   │   │   ├── index.css
│   │   │   │   │   ├── login.css
│   │   │   │   │   ├── place.css
│   │   │   │   │   ├── review.css
│   │   │   │   │   ├── styles.css
│   │   │   │   ├── images/
│   │   │   │   │   ├── cozy-home.png
│   │   │   │   │   ├── favicon.png
│   │   │   │   │   ├── hbnb_default_img.png
│   │   │   │   │   ├── logo.png
│   │   │   │   │   ├── modern-home.png
│   │   │   │   │   ├── summer-house.png
│   │   │   │   │   ├── sweekend-getaway.png
│   │   │   │   ├── js/
│   │   │   │   │   ├── helpers.js
│   │   │   │   │   ├── home.js
│   │   │   │   │   ├── place.js
│   │   │   │   │   ├── review.js
│   │   │   │   │   ├── scripts.js
│   │   │   │   │   ├── user.js
│   │   │   ├── templates/
│   │   │   │   ├── add_review.html
│   │   │   │   ├── footer.html
│   │   │   │   ├── header.html
│   │   │   │   ├── index.html
│   │   │   │   ├── login.html
│   │   │   │   ├── place.html
│   │   │   ├── __init__.py                     # Contains def create_app()
│   │   ├── images/                             # Mermaid diagrams
│   │   │   ├── Base.png
│   │   │   ├── Test_understanding.png
│   │   ├── instance/
│   │   │   ├── development.db                   # DB is created here at initialisation
│   │   ├── tests/
│   │   │   ├── api/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── helper_methods.py
│   │   │   │   ├── test_amenity_api.py
│   │   │   │   ├── test_auth_api.py     
│   │   │   │   ├── test_place_api.py
│   │   │   │   ├── test_review_api.py
│   │   │   │   ├── test_user_api.py
│   │   │   ├── models/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── test_amenity_class.py
│   │   │   │   ├── test_place_class.py
│   │   │   │   ├── test_review_class.py
│   │   │   │   ├── test_user_class.py
│   │   │   ├── rendered_html_pages/             # W3C Validations
│   │   │   │   ├── W3C_results/
│   │   │   │   │   ├── add_review_check.pdf
│   │   │   │   │   ├── index_check.pdf
│   │   │   │   │   ├── login_check.pdf
│   │   │   │   │   ├── place_check.pdf
│   │   │   │   │   ├── review_check.pdf
│   │   │   │   ├── rendering_tools/
│   │   │   │   │   ├── render_index.pdf
│   │   │   │   │   ├── render_login.pdf
│   │   │   │   │   ├── render_page_reviews.pdf
│   │   │   │   │   ├── render_place.pdf
│   │   │   │   ├── README.md
│   │   │   │   ├── index_rendered.html
│   │   │   │   ├── login.html
│   │   │   │   ├── place_rendered.html
│   │   │   │   ├── review_rendered.html
│   │   │   ├── __init__.py
│   │   │   ├── curl_tests.md
│   │   │   ├── README.md                       # Testing Guide
│   │   ├── .env-example
│   │   ├── config.py
│   │   ├── README.md                           # Application Run Guide
│   │   ├── requirements.txt
│   │   ├── run.py
│   ├── README.md                               # YOU ARE HERE - Part 4 Project Guide
├── .gitignore
├── README.md                                   # hbnb Project Guide
```

## Part 4 Task Overview

### Build a Simple Web Client

In this phase, you’ll be focusing on the front-end development of your application using **HTML5**, **CSS3**, and **JavaScript ES6**. Your task is to design and implement an interactive user interface that connects with the back-end services you developed in previous parts of the project.

---

#### Objectives

- Develop a user-friendly interface following provided design specifications.
- Implement client-side functionality to interact with the back-end API.
- Ensure secure and efficient data handling using JavaScript.
- Apply modern web development practices to create a dynamic web application.

---

#### Learning Goals

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

### Database Setup (Seed Data)
- To seed the database with mock users, amenities, places and reviews: 
    - From the project root `part4/hbnb`:
    ```
    python3 seed.py
    ```

- **Notes:** 
    - `Review` model uses positional args: `Review(rating, text, place_id, user_id)`. Please add Places first, then assign Amenities later in a separate step to avoid SA warnings.

---

### Notes

When testing your client against your API, you’ll probably encounter a **Cross-Origin Resource Sharing (CORS)** error.  
You’ll need to modify your API code to allow your client to fetch data from it.

For a deeper understanding of CORS and how to configure your Flask API, refer to external resources such as tutorials and documentation.

---

### Resources

[HTML5 Documentation](https://developer.mozilla.org/en-US/docs/Glossary/HTML5) 
[CSS3 Documentation](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS3)
[JavaScript ES6 Features](https://developer.mozilla.org/en-US/docs/Web/JavaScript/New_in_JavaScript/ECMAScript_2015) 
[Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)
[Responsive Web Design Basics](https://web.dev/articles/responsive-web-design-basics)
[Handling Cookies in JavaScript](https://developer.mozilla.org/en-US/docs/Web/API/Document/cookie)
[Client-Side Form Validation](https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Forms/Form_validation)

## W3C Validations

We were instructed to ensure that our html files were valid on the W3C Validator. Because our application uses Jinja and Javascript to render html pages dynamically, we've included our [rendered html files](/part4/hbnb/tests/rendered_html_pages/README.md) to support the marking process. 