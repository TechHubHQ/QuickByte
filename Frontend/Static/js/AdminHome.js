document.addEventListener('DOMContentLoaded', function() {
    fetch('/admin/home/data')
        .then(response => response.json())
        .then(data => {
        document.getElementById('total-users').textContent = data.total_users;
        document.getElementById('total-orders').textContent = data.total_orders;
        document.getElementById('total-admins').textContent = data.total_admins;
        document.getElementById('total-items').textContent = data.total_items;
        })
        .catch(error => {
            console.error('Error fetching admin dashboard data:', error);
    });
});

document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.sidenav');
    var instances = M.Sidenav.init(elems, {
        edge: 'left',
        inDuration: 250,
        outDuration: 200
    });
});