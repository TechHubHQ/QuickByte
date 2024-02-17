function uploadImage() {
  var form = document.getElementById("profile-image-form");
  var formData = new FormData(form);

  fetch("/upload_image", {
    method: "POST",
    body: formData
  })
  .then(response => response.json())
  .then(data => {
    document.getElementById("upload-message").innerText = data.message;
    // Remove message after 1 seconds
    setTimeout(function() {
      document.getElementById("upload-message").innerText = "";
    }, 1000);
  })
  .catch(error => {
    console.error("Error:", error);
    document.getElementById("upload-message").innerText = "An error occurred while uploading the image.";
  });
}