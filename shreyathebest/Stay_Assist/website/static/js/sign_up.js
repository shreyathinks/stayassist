document.addEventListener("DOMContentLoaded", function () {
    const genderSelect = document.getElementById("gender");
    const hostelSelect = document.getElementById("hostel");

    const hostels = {
        "Men": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T"],
        "Ladies": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
    };

    genderSelect.addEventListener("change", function () {
        hostelSelect.innerHTML = '<option value="" disabled selected>Select Hostel</option>';
        const selectedGender = genderSelect.value;
        
        if (selectedGender) {
            hostels[selectedGender].forEach(block => {
                let option = document.createElement("option");
                option.value = block;
                option.textContent = `Block ${block}`;
                hostelSelect.appendChild(option);
            });
        }
    });

    // Handle form submission
    document.getElementById("register-form").addEventListener("submit", function(event) {
        // Perform any client-side validation here
        const password = document.getElementById("password-group").value;
        if (password.length < 8) {
            alert("Password must be at least 8 characters long.");
            event.preventDefault(); // Prevent form submission if validation fails
        }
        // If validation passes, the form will submit normally
    });
});