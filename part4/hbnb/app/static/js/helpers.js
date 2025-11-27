function getCookie(name) {
    const cookies = document.cookie.split("; ");
    for (const cookie of cookies) {
        const [cookieName, cookieValue] = cookie.split("=");
        if (cookieName === name) return cookieValue;
    }
    return null;
}

/* Check user authentication */
function checkAuthentication(page) {
    const token = getCookie("token");
    
    // Hide the review section on the place details page if the user isn't authenticated
    if (page === 'place') {
        // const reviewButton = document.getElementById("review-button");
        const reviewSection = document.getElementById("review-button-section");
        const reviewButton = document.getElementById("review-button");
        
        // Only modify the DOM if the button actually exists on this page
        if (reviewSection) reviewSection.style.display = token ? "block" : "none";
        if (reviewButton) reviewButton.style.display = token ? "block" : "none";
    }
    
    // Hide the login link on every page if the user is authenticated
    document.getElementById("login-link").style.display = token ? "none" : "block";

    return token;
}
