/* ====== REVIEW SECTION ====== */
// Show review form when button clicked 
document.addEventListener('DOMContentLoaded', () => {

    // redirect unauthenticated users to index page
    const token = getCookie("token");
    if(!token) {
        alert("Please log in first to leave a review.");
        window.location.href = "/";
        return;      // stop running the script
    }

    const reviewForm = document.getElementById('review-form');

    // Get place ID from the URL
    const params = new URLSearchParams(window.location.search);
    const placeId = params.get("place_id");

    // Click rating stars
    const stars = document.querySelectorAll("#overall-rating span");
    const ratingInput = document.getElementById("rating");

    stars.forEach(star => {
        star.addEventListener("click", () => {
            const selectedValue = parseInt(star.dataset.value);

            // if user clicks the same star, then unselect the current star
            if (parseInt(ratingInput.value) === selectedValue) {
                const newValue = selectedValue - 1;
                ratingInput.value = newValue;

                stars.forEach(s => {
                    s.classList.toggle(
                        "selected",
                        parseInt(s.dataset.value) <= newValue
                    )
                });
                return;
            }
            // otherwise select star
            ratingInput.value = selectedValue;

            // color the stars
            stars.forEach(s => {
                s.classList.toggle("selected", parseInt(s.dataset.value) <= selectedValue);
            });
        });
    })
    
    // Handle submission
    if (reviewForm) {
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const token = getCookie('token');
            const text = document.getElementById('review-text').value;
            const rating = parseInt(document.getElementById('rating').value, 10);
            
            if (!text) {
                alert("Please write a comment before submitting");
                return;
            }

            if (rating === 0) {
                alert("Please select a star rating.");
                return;
            }
            
            const submitted = await submitReview(token, placeId, text, rating);
                
            if (submitted) {
                // Show success message and redirect to place popup
                const popup = document.getElementById("success-popup");
                const backBtn = document.getElementById("back-popup")

                if (popup) {
                    popup.classList.remove("popup-hidden");

                    if (backBtn) {
                        backBtn.onclick = () => {
                            window.location.href = `/place?place_id=${placeId}`;
                        };
                    }
                }
                // Clear the form
                document.getElementById('review-text').value = "";
                document.getElementById('rating').selectedIndex = 0;
                stars.forEach(s => s.classList.remove("selected"));
            }
        });
    }
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

        const response = await fetch("/api/v1/reviews", {
            method: "POST",
            headers: headers,
            body: JSON.stringify({
                place: placeId,
                text: reviewText,
                rating: parseInt(rating, 10),
            })
        });
        
        // if the response isn't ok, show the server error and return false
        if (!response.ok) {
            const error = await response.json();
            alert(error.error || "Failed to submit review");
            return false;
        }

        // if response ok, then parse JSON
        const data = await response.json();
        return data;   // return full review JSON object

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
