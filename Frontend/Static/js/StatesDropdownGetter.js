// Fetch JSON data
var jsonData; // Declare a global variable to store the fetched data

fetch("../../Static/Json/Dist_States.json")
  .then(response => response.json())
  .then(data => {
    jsonData = data; // Store the data in the global variable

    // Populate state dropdown
    var stateDropdown = document.getElementById("stateDropdown");
    jsonData.states.forEach(state => {
      var option = document.createElement("option");
      option.value = state.state;
      option.textContent = state.state;
      stateDropdown.appendChild(option);
    });

    // Initial population of districts based on the first state
    updateDistricts();
  })
  .catch(error => console.error("Error fetching JSON data:", error));

// Function to update the districts dropdown based on the selected state
function updateDistricts() {
  var stateDropdown = document.getElementById("stateDropdown");
  var districtDropdown = document.getElementById("districtDropdown");
  var selectedState = stateDropdown.value;

  // Find the selected state in JSON data
  var selectedStateObj = jsonData.states.find(function (stateObj) {
    return stateObj.state === selectedState;
  });

  // Clear previous districts
  districtDropdown.innerHTML = '<option value="">Select District</option>';

  // Populate districts for the selected state
  if (selectedStateObj) {
    selectedStateObj.districts.forEach(function (district) {
      var option = document.createElement("option");
      option.value = district;
      option.textContent = district;
      districtDropdown.appendChild(option);
    });
  }
}
