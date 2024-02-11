document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('user-login-form');

    form.addEventListener('submit', function (event) {
        event.preventDefault();

        const formData = new FormData(form);
        for (const [key, value] of formData.entries()) {
            console.log(`${key}: ${value}`);
        }
    });

    // Add event listeners for input focus and blur
    const inputFields = form.querySelectorAll('input');
    inputFields.forEach(inputField => {
        inputField.addEventListener('focus', handleInputFocus);
        inputField.addEventListener('blur', handleInputBlur);
    });
});

// Function to handle input focus
function handleInputFocus(event) {
    const label = event.target.nextElementSibling;
    label.style.transform = 'translateY(-24px)';
    label.style.fontSize = '14px';
}

// Function to handle input blur
function handleInputBlur(event) {
    const input = event.target;
    const label = input.nextElementSibling;

    if (!input.value.trim()) {
        label.style.transform = 'translateY(0)';
        label.style.fontSize = '16px';
    }
}
