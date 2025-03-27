document.addEventListener("DOMContentLoaded", function () {
    const authForm = document.getElementById("auth-form");
    const toggleText = document.getElementById("toggle-text");
    const authTitle = document.getElementById("auth-title");

    // Get the 'type' query parameter from the URL
    const urlParams = new URLSearchParams(window.location.search);
    const userType = urlParams.get('type');  // 'buyer' or 'seller'
    
    // If no 'type' parameter is provided or invalid type, handle it
    if (!userType || (userType !== 'buyer' && userType !== 'seller')) {
        alert("Invalid or missing user type!");
        return;  // Optionally, redirect to a safe page or show an error
    }

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
            body: JSON.stringify({ username, password, user_type }),
            mode: "cors"
        });

        const result = await response.json();
        

        console.log(result);
        console.log(userType);
        // Redirect based on user type
        if (result.success) {
            if (!isSignUp){
                if (result.role === userType && userType === 'seller') {
                    console.log('seller')
                    alert(result.message || result.error);
                    window.location.href = "seller_dashboard.html";  // Redirect seller to dashboard
                } else if (result.role === userType && userType === 'buyer'){
                    console.log('buyer')
                    alert(result.message || result.error);
                    window.location.href = "buyer_dashboard.html";  // Redirect buyer to their page
                }
                else{
                    alert("Unauthorized!!")
                }
            }else{
                alert("User Created successfully!")
            }
        }else{
            if(isSignUp){
                alert("Sign Up Failed!")
            }else{
                alert("Login Failed!")
            }
        }
    });
});
