/* 
    This is a SAMPLE FILE to get you started.
    Please, follow the project instructions to complete the tasks.
*/

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
  
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            // --- Client-side validation ---
            if (!email || !password) {
                alert("Email and password are required.");
                return;
            }

            await loginUser(email, password);
        });
    }

    async function loginUser(email, password) {
        try {
            const response = await fetch('/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            });
            if (response.ok) {
                const data = await response.json();

                document.cookie = `token=${data.access_token}; path=/`; // assigns JWT to cookie
                window.location.href = 'index.html';                   // redirects user after login
            } else {
                alert('Login failed: ' + response.statusText);         // handles server responses
            }
        } catch (error) {
            alert('Network error: ' + error.message);                  // handles network failures
        }
    }
});
