document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("login-form");

    form.addEventListener("submit", function (event) {
        event.preventDefault(); // Prevents form from actually submitting to a backend

        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;

        if (email === "" || password === "") {
            alert("Please fill in all fields.");
            return;
        }

        // Simulated login logic (Replace with actual backend authentication)
        if (email === "user@example.com" && password === "password123") {
            alert("Login successful!");
            window.location.href = "features.html"; // Redirect to dashboard
        } else {
            alert("Invalid email or password.");
        }
    });
});
