/* ====== HOMEPAGE ====== */

/* Check user authentication */
function checkAuthentication() {
    const token = getCookie("token");
    const loginLink = document.getElementById("login-link");

    if (!token) {
        loginLink.style.display = "block";
    } else {
        loginLink.style.display = "none";
    }

    // return token;
    fetchPlaces(token);
}

/* Get cookie */
function getCookie(name) {
    const cookies = document.cookie.split("; ");
    for (const cookie of cookies) {
        const [cookieName, cookieValue] = cookie.split("=");
        if (cookieName === name) return cookieValue;
    }
    return null;
}

// Fetch places for homepage
async function fetchPlaces(token) {
    try {
        const headers = { 'Content-Type': 'application/json' };

        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch('/api/v1/places/', {
            method: 'GET',
            headers
        });

        if (!response.ok) {
            throw new Error(`HTTP error: ${response.status}`);
        }
        
        const places = await response.json();
        displayPlaces(places);

    } catch (error) {
        console.error('Error fetching places:', error);
        throw error;
    }
}
        
// Display places on homepage
async function displayPlaces(places) {
    // Remove all .place-card divs from .place-list parent
    let section = document.querySelector('.places-list');

    while (section.hasChildNodes()) {
        section.removeChild(section.firstChild);
    }

    // Dynamically create html for each place in places
    for (i = 0; i < places.length; i++) {
        p = places[i];

        // Create elements
        const place = document.createElement('div');  // Create a div element for the property
        const link = document.createElement('a');  // Create a link to the property's page
        const image = document.createElement('img');  // Create an image of the property
        const title = document.createElement('h2');  // Create the name
        const description = document.createElement('p');  // Create the description
        const price = document.createElement('p');  // Create the price
    
        // Set attributes and values for html tags
        place.setAttribute('class', 'places-card');
        link.href = `/place?place_id=${p['id']}`;
        if (p['image_url']) { 
            image.src = `/static/${p['image_url']}`;
        } else {
            image.src = '/static/images/logo.png';  // Set default image to logo if place image not found
        }
        image.alt = "Image of " + p['title'];
        image.height = 200;
        image.width = 300;
        title.innerHTML = p['title'];
        description.innerHTML = p['description'];
        price.innerHTML = p['price'];
    
        
        // Insert the place within .places-list section
        placesList = document.querySelector('.places-list');
        placesList.appendChild(place).appendChild(link).appendChild(image);
        placesList.appendChild(place).appendChild(title);
        placesList.appendChild(place).appendChild(description);
        placesList.appendChild(place).appendChild(price);
    }
}

checkAuthentication();
