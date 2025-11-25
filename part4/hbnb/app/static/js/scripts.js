/* ====== PLACES SECTION ====== */
/* Loads all places from the API and displays them on the page */
document.addEventListener("DOMContentLoaded", () => {
    fetch("/api/v1/places/")
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById("place-details");

            data.forEach(place => {
                const div = document.createElement("div");
                div.className = "place-card";

                div.innerHTML = `
                    <h2>${place.title}</h2>
                    <p>${place.description}</p>
                    <p>Price: $${place.price}</p>
                `;

                container.appendChild(div);
            });
        })
        .catch(err => console.error(err));
});


/* Get place ID from URL */
function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get("id");
}

/* Check user authentication */
function checkAuthentication() {
    const token = getCookie('token');
    const addReviewSection = document.getElementById('add-review');

    if (!token) {
        addReviewSection.style.display = 'none';
    } else {
        addReviewSection.style.display = 'block';
        // Store the token for later use
        fetchPlaceDetails(token, placeId);
    }
}

function getCookie(name) {
    const cookies = document.cookie.split('; ');
    for (const cookie of cookies) {
        const [cookieName, cookieValue] = cookie.split('=');
        if (cookieName === name) {
            return cookieValue;
        }
    }

    return null;
}

/* Fetch place details */
async function fetchPlaceDetails(token, placeId) {
    try {
        const response = await fetch(`/api/v1/places/${placeId}`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authorization": token ? `Bearer ${token}` : ""
            }
        });

        const data = await response.json();
        displayPlaceDetails(data);

    } catch (error) {
        console.error("Error fetching place:", error);
    }
}

/* Populate place details */
function displayPlaceDetails(place) {
    const container = document.querySelector('#place-details');
    container.innerHTML = "";

    const nameEl = document.createElement('h2');
    nameEl.textContent = place.name;

    const descEl = document.createElement('p');
    descEl.textContent = place.description;

    const priceEl = document.createElement('p');
    priceEl.textContent = `Price per night: $${place.price}`;

    const amenitiesTitle = document.createElement('h3');
    amenitiesTitle.textContent = "Amenities";

    const amenitiesList = document.createElement('ul');
    place.amenities.forEach(a => {
        const li = document.createElement('li');
        li.textContent = a.name || a;
        amenitiesList.appendChild(li);
    });

    container.appendChild(nameEl);
    container.appendChild(descEl);
    container.appendChild(priceEl);
    container.appendChild(amenitiesTitle);
    container.appendChild(amenitiesList);

    // Call separate function for reviews
    displayReviews(place.reviews);
}

function displayReviews(reviews) {
    const reviewsContainer = document.querySelector('#reviews');
    reviewsContainer.innerHTML = "";

    const title = document.createElement('h3');
    title.textContent = "Reviews";

    reviewsContainer.appendChild(title);

    reviews.forEach(r => {
        const p = document.createElement('p');
        p.textContent = `${r.text} (Rating: ${r.rating})`;
        reviewsContainer.appendChild(p);
    });
}

document.addEventListener('DOMContentLoaded', () => {                   // wait for DOM(document) to load
    const loginForm = document.getElementById('login-form');            // take login form from HTML

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();                                     // run our custom logic rather than browser default
  
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            await loginUser(email, password);                           // pass entered values to loginUser
        });
    }

    async function loginUser(email, password) {
        try {
            const response = await fetch('/api/v1/auth/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            });                                                         // send login request

            if (response.ok) {
                const data = await response.json();                     // parse JSON data
                document.cookie = `token=${data.access_token}; path=/`; // assign token to cookie
                window.location.href = 'index.html';                    // redirect user to index.html
            } else {
                alert((await response.json()).error || 'Login failed');
            }
        } catch (error) {
            alert('Network error: ' + error.message);                   // network error if catch fails
        }
    }
})
