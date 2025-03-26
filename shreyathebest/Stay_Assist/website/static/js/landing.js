function showServiceDetails(service) {
  const detailsPanel = document.getElementById("serviceDetails");
  const title = document.getElementById("serviceTitle");
  const description = document.getElementById("serviceDescription");

  // Set content based on service type
  switch (service) {
    case "repairs":
      title.textContent = "Repair Services";
      description.textContent =
        "Request quick repairs for plumbing issues, furniture, electrical problems, and more. Our skilled maintenance staff will address your concerns promptly to ensure your living space remains comfortable and functional.";
      break;
    case "cleaning":
      title.textContent = "Cleaning Services";
      description.textContent =
        "Schedule regular or one-time cleaning services for your room. Our professional cleaning staff uses eco-friendly products to ensure your space is spotless, sanitized, and fresh.";
      break;
    case "laundry":
      title.textContent = "Laundry Services";
      description.textContent =
        "Convenient laundry and dry cleaning pickup and delivery services. Schedule pickups, track your order, and receive notifications when your clean clothes are ready to be delivered back to your room.";
      break;
    case "pest":
      title.textContent = "Pest Control Services";
      description.textContent =
        "Professional pest control services to keep your living space free from unwanted guests. Our treatments are safe, effective, and environmentally responsible.";
      break;
  }

  // Show the panel
  detailsPanel.classList.add("active");
}

function hideServiceDetails() {
  const detailsPanel = document.getElementById("serviceDetails");
  detailsPanel.classList.remove("active");
}
function redirectTo(url) {
  window.location.href = url;
}
