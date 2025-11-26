/* ====== HOMEPAGE ====== */
document.addEventListener("DOMContentLoaded", () => {
    const token = checkAuthentication('home');     // Show/hide login link

    fetchPlaces(token);
    priceList();
});

/* Filter by price */
document.querySelector('.price-filter').addEventListener('change', (event) => {
    // Get the selected price value
    priceFilter = event.target.value;

    // Iterate over the places and show/hide them based on the selected price
    places = document.querySelectorAll('.places-card');
    places.forEach(place => {
        const priceText = place.querySelector('.price').textContent.trim();  // Fetch price from html
        const price = Number(priceText.replace(/[^0-9.]/g, ''));  // Ensure that price is a number

        if (priceFilter === 'All') {
            place.hidden = false;
            return;
        }

        const limit = Number(priceFilter.replace(/[^0-9.]/g, ''));
        place.hidden = price > limit;
    });
});


/* Dynamically create price filter options */
async function priceList() {
    const priceList = document.querySelector('.price-filter');
    const options = [10, 50, 100, "All"];

    for (let i = 0; i < options.length; i++) {
        let option = document.createElement('option');
        option.value = options[i];
        option.innerHTML = `$${options[i]}`;
        priceList.appendChild(option);
    }

    priceList.name = "price-filter";  // needed to reference the form data after the form is submitted
    priceList.id = "prices";  // needed to associate the drop-down list with a label
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
    
        // Set class attributes for ease of css selection
        place.setAttribute('class', 'places-card');
        place.setAttribute('id', p['id']);
        price.setAttribute('class', 'price');
        title.setAttribute('class', 'title');
        description.setAttribute('class', 'description');
        link.setAttribute('class', 'link-to-place-page');
        image.setAttribute('class', 'place-photo');

        // Set up image as a link to place page
        link.href = `/place?place_id=${p['id']}`;
        if (p['image_url']) { 
            image.src = `/static/${p['image_url']}`;
        } else {
            image.src = '/static/images/logo.png';  // Set default image to logo if place image not found
        }
        image.alt = "Image of " + p['title'];
        image.height = 200;
        image.width = 300;

        // Set tag contents
        title.innerHTML = p['title'];
        description.innerHTML = p['description'];
        price.innerHTML = `$${p['price']}`;
        
        // Insert the place within .places-list section
        placesList = document.querySelector('.places-list');
        placesList.appendChild(place).appendChild(link).appendChild(image);
        placesList.appendChild(place).appendChild(title);
        placesList.appendChild(place).appendChild(description);
        placesList.appendChild(place).appendChild(price);
    }
}

checkAuthentication();
