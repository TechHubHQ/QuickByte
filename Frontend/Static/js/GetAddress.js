document.addEventListener("DOMContentLoaded", function () {
    const addressBox = document.getElementById("address-box");
    const editForm = document.getElementById("edit-form");
    const editButton = document.getElementById("edit-button");

    // Fetch the user's address data
    fetch("/my_address_data")
      .then((response) => response.json())
      .then((data) => {
        if (data.error) {
          addressBox.textContent = data.error;
        } else {
          data.forEach((address) => {
            const addressDetails = document.createElement("div");
            addressDetails.innerHTML = `
              <p><strong>Address Line 1:</strong> ${address.address_line1}</p>
              <p><strong>Landmark:</strong> ${address.address_landmark}</p>
              <p><strong>State:</strong> ${address.state}</p>
              <p><strong>District:</strong> ${address.district}</p>
            `;
            addressBox.appendChild(addressDetails);
          });
        }
      })
      .catch((error) => {
        addressBox.textContent = "Error fetching address data";
        console.error("Error:", error);
      });

    // Show edit form and hide address details
    document.getElementById("edit-button").addEventListener("click", function () {
      editForm.style.display = "block";
      addressBox.style.display = "none";
      editButton.style.display = "none";
    });

    // Hide edit form and show address details
    document.getElementById("back-button").addEventListener("click", function () {
      editForm.style.display = "none";
      addressBox.style.display = "block";
      editButton.style.display = "block";
    });

    // Redirect after saving changes
    document.getElementById("update-form").addEventListener("submit", function () {
      window.location.href = "/my_address_data";
    });
});
