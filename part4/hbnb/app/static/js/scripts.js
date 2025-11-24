/* 
    This is a SAMPLE FILE to get you started.
    Please, follow the project instructions to complete the tasks.
*/

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const reviewForm = document.getElementById('review-form');
    let placeId = null;

    // login form submission
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            // Placeholder to add logic to handle form submission (Task 1)
        })
    }

    // review form submission
    if (reviewForm) {
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            
            const token = getCookie('token');
            const text = document.getElementById('review-text');
            const rating = parseInt(document.getElementById('rating').value, 10);

            if (!text.value) {
                alert("Please write your comment")
            } else {
                const submit = await submitReview(token, placeId, text.value, rating);

                if (submit) {
                    text.value = "";
                    document.getElementById('rating').selectedIndex = 0;
                }
            }
        });
    }

    // leave a review button
    const showFormBtn = document.getElementById('show-form-btn');
    const reviewFormSection = document.getElementById('review-form-section');

    if (showFormBtn && reviewFormSection) {
        showFormBtn.addEventListener('click', () => {
            showFormBtn.style.display = 'none';
            reviewFormSection.classList.remove('hidden');
        });
    }
    checkAuthentication();
    });

// Make the AJAX requests to the API
async function loginUser(email, password) {
    const response = await fetch('https://', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
    });
    // Handle the API response and store the token in a cookie
    if (response.ok) {
        const data = await.response.json();
        document.cookie = `token=${data.access_token}; path=/`;
        window.location.href = 'index.html';
    } else {
        alert
    }
}

// Check user authentication
function checkAuthentication() {
    const token = getCookie('token');
    const path = window.location.pathname;
    const loginLink = document.getElementById('login-link');
    const addReviewSection = document.getElementById('add-review');

    // if user tried to add review and not logged in, redirect them to home
    if (window.location.pathname.includes('add_review') && !token) {
        window.location.href = 'index';
        return;
    }

    // if user is not logged in
    if (!token) {
        addReviewSection.style.display = 'none';
    } else {
        addReviewSection.style.display = 'block';
    }
}

function getCookie(name) {
    // Function to get a cookie value by its name
    // Your code here
}

// Fetch places data
async function fetchPlaces(token) {
    // Make a GET request to fetch places data
    // Include the token in the Authorization header
    // Handle the response and pass the data to displayPlaces function
}

// Populate places list
function displayPlaces(places) {
    // Clear the current content of the places list
    // Iterate over the places data
    // For each place, create a div element and set its content
    // Append the created element to the places list
}

// Get place ID from URL
function getPlaceIdFromURL() {
    // Extract the place ID from window.location.search
    // Your code here
}

// Fetch place details
async function fetchPlaceDetails(token, placeId) {
    // Make a GET request to fetch place details
    // Include the token in the Authorization header
    // Handle the response and pass the data to displayPlaceDetails function
}

// Populate place details
function displayPlaceDetails(place) {
    // Clear the current content of the place details section
    // Create elements to display the place details (name, description, price, amenities and reviews)
    // Append the created elements to the place details section
    ('Login failed: ' + response.statusText);
}

// Make AJAX request to submit review
async function submitReview(token, placeId, reviewText, rating) {
    try{
        let headers = {
            'Content-Type': 'application/json',
        };
        if (token) {
            headers['Authorization'] = `Bearer ${token}`
        }
        console.log('Sending token:', token);
        console.log('Headers:', headers);
        const response = await fetch('http://localhost:5000/api/v1/reviews', {
            method: 'POST',
            headers: headers,
            body: JSON.stringify({
                place_id: placeId,
                text: reviewText,
                rating: rating
            })
        });
        // Handle the API response
        if (!response.ok) {
            alert('Review submission failed');
            return false;
        }
        const data = await response.json();
        alert('Review submission successful');
        return true;
    } catch (error) {
        console.log('Error:', error);
        return false;
    }
}