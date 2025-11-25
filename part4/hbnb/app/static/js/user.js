/* ====== LOGIN SECTION ====== */
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
                window.location.href = '/';                    // redirect user to index.html
            } else {
                alert((await response.json()).error || 'Login failed');
            }
        } catch (error) {
            alert('Network error: ' + error.message);                   // network error if catch fails
        }
    }
})