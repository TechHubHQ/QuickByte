document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('admin-login-form');
  
    form.addEventListener('submit', async (event) => {
      event.preventDefault();
  
      const username = document.getElementById('username').value;
      const password = document.getElementById('password').value;
  
      try {
        const response = await fetch('/admin/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ username, password })
        });
  
        if (response.ok) {
          const { token } = await response.json();
          // Store the token in local storage or session storage
          localStorage.setItem('adminToken', token);
          // Redirect the user to the admin dashboard
          window.location.href = '/admin/dashboard';
        } else {
          const { error } = await response.json();
          M.toast({ html: error });
        }
      } catch (error) {
        console.error('Error logging in:', error);
        M.toast({ html: 'An error occurred during login. Please try again.' });
      }
    });
  });