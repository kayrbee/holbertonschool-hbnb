/* ====== PLACES SECTION ====== */
/* Loads all places from the API and displays them on the page */
document.addEventListener("DOMContentLoaded", () => {
    const placeId = getPlaceIdFromURL();     // Extract ?place_id=xxx
    const token = checkAuthentication();     // Show/hide review form
    fetchPlaceDetails(token, placeId);       // Load the place details
});

/* Get place ID from URL */
function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get("place_id");
}

/* Check user authentication */
function checkAuthentication() {
    const token = getCookie("token");
    const addReviewSection = document.getElementById("add-review");

    if (!token) {
        addReviewSection.style.display = "none";
    } else {
        addReviewSection.style.display = "block";
    }

    return token;
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

        const place = await response.json();

        displayPlaceDetails(place);

    } catch (error) {
        console.error("Error fetching place:", error);
    }
}

/* Populate place details */
function displayPlaceDetails(place) {
    const container = document.getElementById("place-details");
    container.innerHTML = "";

    // Title
    const title = document.createElement("h2");
    title.textContent = place.title;
    container.appendChild(title);

    // Image
    if (place.image_url) {
        const img = document.createElement("img");
        img.src = `/static/${place.image_url}`;
        img.alt = place.title;
        img.className = "place-photo";
        container.appendChild(img);
    }

    // Host
    const host = document.createElement("p");
    host.innerHTML = `<strong>Host:</strong> ${place.user.first_name} ${place.user.last_name}`;
    container.appendChild(host);

    // Price
    const price = document.createElement("p");
    price.innerHTML = `<strong>Price per night:</strong> $${place.price}`;
    container.appendChild(price);

    // Description
    const desc = document.createElement("p");
    desc.textContent = place.description;
    container.appendChild(desc);

    // Amenities
    const amenitiesHeader = document.createElement("h3");
    amenitiesHeader.textContent = "Amenities";
    container.appendChild(amenitiesHeader);

    const amenitiesList = document.createElement("ul");
    place.amenities.forEach(a => {
        const li = document.createElement("li");
        li.textContent = a.name;
        amenitiesList.appendChild(li);
    });
    container.appendChild(amenitiesList);

    // Reviews
    displayReviews(place.reviews);
}

/* Shows all reviews OR a message if none exist */
function displayReviews(reviews) {
    const container = document.getElementById("reviews");
    container.innerHTML = "";

    const header = document.createElement("h3");
    header.textContent = "Reviews";
    container.appendChild(header);

    if (!reviews || reviews.length === 0) {
        container.appendChild(document.createTextNode("This place has no reviews."));
        return;
    }

    reviews.forEach(r => {
        const div = document.createElement("div");
        div.className = "review-card";

        div.innerHTML = `
            <p><strong>${r.user.first_name} ${r.user.last_name}</strong></p>
            <p>Rating: ${r.rating}/5</p>
            <p>"${r.text}"</p>
        `;

        container.appendChild(div);
    });
}