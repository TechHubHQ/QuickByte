var jsonData;

fetch("../../Static/Json/Support_Issues.json")
  .then(response => response.json())
  .then(data => {
    jsonData = data; // Store the data in the global variable

    // Populate category dropdown
    var categoryDropdown = document.getElementById("category");
    jsonData.categories.forEach(category => {
      var option = document.createElement("option");
      option.value = category.name; // Use category.name
      option.textContent = category.name; // Use category.name
      categoryDropdown.appendChild(option);
    });

    // Initial population of sub cats based on the first category
    updateSubCat();
  })
  .catch(error => console.error("Error fetching JSON data:", error));

// Function to update the subcategories dropdown based on the selected category
function updateSubCat() {
  var categoryDropdown = document.getElementById("category");
  var subcategoryDropdown = document.getElementById("subcategory");
  var selectedCategory = categoryDropdown.value;

  // Find the selected category in JSON data
  var selectedCatObj = jsonData.categories.find(function (catObj) {
    return catObj.name === selectedCategory; // Use catObj.name
  });

  // Clear previous subcategories
  subcategoryDropdown.innerHTML = '<option value="">Select Sub Category</option>';

  // Populate subcategories for the selected category
  if (selectedCatObj) {
    selectedCatObj.subcategories.forEach(function (subcategory) {
      var option = document.createElement("option");
      option.value = subcategory;
      option.textContent = subcategory;
      subcategoryDropdown.appendChild(option);
    });
  }
}
