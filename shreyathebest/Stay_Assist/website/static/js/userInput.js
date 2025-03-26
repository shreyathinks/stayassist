function toggleImageUpload() {
    var serviceType = document.getElementById("service_type").value;
    var imageUploadDiv = document.getElementById("image-upload");

    // Show image upload only for Electrical Repair or Furniture Repair
    if (serviceType === "Electrical Repair" || serviceType === "Furniture Repair") {
        imageUploadDiv.style.display = "block";
    } else {
        imageUploadDiv.style.display = "none";
    }
}