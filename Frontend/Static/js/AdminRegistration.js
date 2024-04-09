document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('admin-register-form');
  
    form.addEventListener('submit', async (event) => {
      event.preventDefault();
  
      const username = document.getElementById('username').value;
      const email = document.getElementById('email').value;
      const password = document.getElementById('password').value;
  
      try {
        const response = await fetch('/admin/register', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ username, email, password })
        });
  
        if (response.ok) {
          M.toast({ html: 'Admin registered successfully!' });
          setTimeout(() => {
            window.location.href = '/admin/login';
          }, 2000);
          
        } else {
          const { error } = await response.json();
          M.toast({ html: error });
        }
      } catch (error) {
        console.error('Error registering admin:', error);
        M.toast({ html: 'An error occurred during registration. Please try again.' });
      }
    });
  });