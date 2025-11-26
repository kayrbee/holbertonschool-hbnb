/* ====== REVIEW SECTION ====== */
// Show review form when button clicked 
document.addEventListener('DOMContentLoaded', () => {
    const showFormBtn = document.getElementById("show-form-btn");
    const reviewFormSection = document.getElementById("review-form-section");
    const reviewForm = document.getElementById('review-form');

    // Get place ID from the URL
    const params = new URLSearchParams(window.location.search);
    const placeId = params.get("place_id");

    // Show form on button click
    if (showFormBtn && reviewFormSection) {
        showFormBtn.addEventListener("click", () => {
            reviewFormSection.style.display = "block";
            showFormBtn.style.display = "none";
        });
    }

    // Click rating stars
    const stars = document.querySelectorAll("#overall-rating span");
    const ratingInput = document.getElementById("rating");

    stars.forEach(star => {
        star.addEventListener("click", () => {
            const selectedValue = parseInt(star.dataset.value);
            // update the hidden rating input
            ratingInput.value = selectedValue;

            // color the stars
            stars.forEach(s => {
                s.classList.toggle("selected", parseInt(s.dataset.value) <= selectedValue);
            });
        });
    })
    
    // Handles submission
    if (reviewForm) {
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const token = getCookie('token');
            const text = document.getElementById('review-text').value;
            const rating = parseInt(document.getElementById('rating').value, 5);
            
            if (!text) {
                alert("Please write a comment before submitting");
                return;
            }
            
            const submitted = await submitReview(token, placeId, text, rating);
                
            if (submitted) {
                // Clear the form
                document.getElementById('review-text').value = "";
                document.getElementById('rating').selectedIndex = 0;
            }
        });
    }
    checkAuthentication();
});

// Make AJAX request to submit review
// Use the Fetch API to send a POST request with the review data
async function submitReview(token, placeId, reviewText, rating) {
    try {
        const headers = {
            'Content-Type': 'application/json',
        };

        if (token) {
            headers['Authorization'] = `Bearer ${token}`
        }

        const response = await fetch("http://localhost:5000/api/v1/reviews", {
            method: "POST",
            headers: headers,
            body: JSON.stringify({
                place_id: placeId,
                text: reviewText,
                rating: parseInt(rating, 5),
            })
        });
        
        return await handleResponse(response);

    } catch (error) {
        console.error("Network Error:", error);
        alert("Network error while submitting review.");
        return false;
    }
}

// Handle API Response
async function handleResponse(response) {
    if (!response.ok) {
        const errorData = await response.json();
        alert(errorData.error || "Failed to submit review");
        return false;
    }

    alert("Review submitted successfully");
    return true;
}
