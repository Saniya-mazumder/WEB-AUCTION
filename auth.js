document.addEventListener("DOMContentLoaded", function () {
    const authForm = document.getElementById("auth-form");
    const toggleText = document.getElementById("toggle-text");
    const authTitle = document.getElementById("auth-title");

    let isSignUp = false;

    toggleText.addEventListener("click", function (event) {
        event.preventDefault();
        isSignUp = !isSignUp;
        authTitle.textContent = isSignUp ? "Sign Up" : "Sign In";
        toggleText.innerHTML = isSignUp 
            ? `Already have an account? <a href="#">Sign In</a>`
            : `Don't have an account? <a href="#">Sign Up</a>`;
    });

    authForm.addEventListener("submit", async function (event) {
        event.preventDefault();
        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;
        const user_type = "seller"; // Change as per selection logic

        const endpoint = isSignUp ? "http://127.0.0.1:5000/register" : "http://127.0.0.1:5000/login";
        const response = await fetch(endpoint, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password, user_type })
        });

        const result = await response.json();
        alert(result.message || result.error);

        console.log(result);
        // Redirect based on user type
        if (result.success) {
            console.log("success");
            if (result.role === 'seller') {
                console.log('seller')
                window.location.href = "seller_dashboard.html";  // Redirect seller to dashboard
            } else {
                
                window.location.href = "buyer_dashboard.html";  // Redirect buyer to their page
            }
        }
    });
});
