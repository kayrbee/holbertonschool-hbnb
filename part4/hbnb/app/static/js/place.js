/* ====== PLACES SECTION ====== */
/* Loads all places from the API and displays them on the page */
document.addEventListener("DOMContentLoaded", () => {
    const placeId = getPlaceIdFromURL();     // Extract ?place_id=xxx
    const token = checkAuthentication();     // Show/hide review button

    const reviewLink = document.getElementById("leave-review-link");
    if (reviewLink && placeId) {
        reviewLink.href = `/add_review?place_id=${placeId}`;
    }

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
    const reviewButton = document.getElementById("review-button");

    if (!token) {
        reviewButton.style.display = "none";
    } else {
        reviewButton.style.display = "block";
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

    // Title
    document.getElementById("place-title").textContent = place.title;

    // Image
    const img = document.getElementById("place-image");
    img.src = `/static/${place.image_url}`;
    img.alt = place.title;

    // Info box (host, price, description)
    const infoBox = document.getElementById("place-info");
    infoBox.innerHTML = `
        <p><strong>Host:</strong> ${place.user.first_name} ${place.user.last_name}</p>
        <p><strong>Price per night:</strong> $${place.price}</p>
        <p>${place.description}</p>
    `;

    // Amenities
    const amenitiesContainer = document.getElementById("amenities-list");
    amenitiesContainer.innerHTML = place.amenities
        .map(a => `<div class="amenity-item">${a.name}</div>`)
        .join("");

    // Reviews
    displayReviews(place.reviews);
}

/* Shows all reviews OR a message if none exist */
function displayReviews(reviews) {
    const container = document.getElementById("reviews-list");
    container.innerHTML = "";

    if (!reviews || reviews.length === 0) {
        container.innerHTML = `<p>No reviews yet.</p>`;
        return;
    }

    reviews.forEach(r => {
        container.innerHTML += `
            <div class="review-card">
                <p><strong>${r.user.first_name} ${r.user.last_name}</strong></p>
                <p>Rating: ${r.rating}/5</p>
                <p>"${r.text}"</p>
            </div>
        `;
    });
}