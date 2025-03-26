document.addEventListener("DOMContentLoaded", function () {
    const urlParams = new URLSearchParams(window.location.search);
    const userType = urlParams.get("type") || "buyer";
    const authTitle = document.getElementById("auth-title");
    const authForm = document.getElementById("auth-form");
    const toggleText = document.getElementById("toggle-text");
    const toggleLink = document.getElementById("toggle-link");
    
    let isSignUp = false;

    function updateForm() {
        authTitle.textContent = isSignUp ? `Sign Up as ${userType}` : `Sign In as ${userType}`;
        toggleText.innerHTML = isSignUp 
            ? `Already have an account? <a href="#" id="toggle-link">Sign In</a>`
            : `Don't have an account? <a href="#" id="toggle-link">Sign Up</a>`;
    }

    toggleText.addEventListener("click", function (event) {
        event.preventDefault();
        isSignUp = !isSignUp;
        updateForm();
    });

    authForm.addEventListener("submit", function (event) {
        event.preventDefault();
        alert(`${isSignUp ? "Signing Up" : "Signing In"} as ${userType}`);
        // Here you can add fetch API calls to interact with MySQL backend
    });

    updateForm();
});
