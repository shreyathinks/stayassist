document.addEventListener("DOMContentLoaded", function () {
    // Select all service cards
    const serviceCards = document.querySelectorAll(".service-card");
    const container = document.querySelector(".container");

    // Create the form dynamically
    const formContainer = document.createElement("div");
    formContainer.classList.add("service-form-container");
    formContainer.innerHTML = `
        <div class="service-form">
            <h2 id="service-title">Book Service</h2>
            <label for="issue">Describe the Issue:</label>
            <textarea id="issue" placeholder="Enter your issue here..." required></textarea>

            <div id="upload-container">
                <label for="upload">Upload an Image (if required):</label>
                <input type="file" id="upload" accept="image/*">
            </div>

            <label for="time-slot">Select a Date & Time:</label>
            <input type="datetime-local" id="time-slot" required>

            <button id="submit-btn">Submit</button>
            <button id="close-btn">Close</button>
        </div>
    `;

    // Append the form container to the main container
    container.appendChild(formContainer);

    // Hide the form initially
    formContainer.style.display = "none";

    // Event listener for clicking service cards
    serviceCards.forEach((card) => {
        card.addEventListener("click", function () {
            const serviceName = card.querySelector("img").alt; // Get service name from alt text
            document.getElementById("service-title").innerText = `Book ${serviceName}`;

            // Hide image upload for Cleaning service
            const uploadContainer = document.getElementById("upload-container");
            if (serviceName.toLowerCase().includes("cleaning")) {
                uploadContainer.style.display = "none";
            } else {
                uploadContainer.style.display = "block";
            }

            formContainer.style.display = "flex"; // Show form
        });
    });

    // Close button functionality
    document.getElementById("close-btn").addEventListener("click", function () {
        formContainer.style.display = "none";
    });
});
