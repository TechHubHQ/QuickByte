document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.sidenav');
    var instances = M.Sidenav.init(elems, {
      edge: 'left',
      inDuration: 250,
      outDuration: 200
    });

    var sidenavTrigger = document.querySelector('.sidenav-trigger');
    sidenavTrigger.addEventListener('click', function() {
      instances[0].open();
    });
  
    fetch('/admin/dashboard/data')
      .then(response => response.json())
      .then(data => {
        const orderTrendsData = {
          labels: data.orderTrends.map(item => item.month),
          datasets: [
            {
              label: 'Orders',
              data: data.orderTrends.map(item => item.orders),
              backgroundColor: 'rgba(54, 162, 235, 0.5)',
              borderColor: 'rgba(54, 162, 235, 1)',
              borderWidth: 1
            }
          ]
        };
  
        const popularDishesData = {
          labels: data.popularDishes.map(item => `${item.dish} (${item.qty})`),
          datasets: [
            {
              label: 'Popularity',
              data: data.popularDishes.map(item => item.orders),
              backgroundColor: [
                'rgba(255, 99, 132, 0.5)',
                'rgba(255, 159, 64, 0.5)',
                'rgba(255, 205, 86, 0.5)',
                'rgba(75, 192, 192, 0.5)',
                'rgba(153, 102, 255, 0.5)'
              ],
              borderColor: [
                'rgb(255, 99, 132)',
                'rgb(255, 159, 64)',
                'rgb(255, 205, 86)',
                'rgb(75, 192, 192)',
                'rgb(153, 102, 255)'
              ],
              borderWidth: 1
            }
          ]
        };
  
        const customerSatisfactionData = {
          labels: ['Excellent', 'Good', 'Fair', 'Poor'],
          datasets: [
            {
              label: 'Customer Satisfaction',
              data: [
                data.customerSatisfaction.excellent,
                data.customerSatisfaction.good,
                data.customerSatisfaction.fair,
                data.customerSatisfaction.poor
              ],
              backgroundColor: [
                'rgba(75, 192, 192, 0.5)',
                'rgba(153, 102, 255, 0.5)',
                'rgba(255, 159, 64, 0.5)',
                'rgba(255, 99, 132, 0.5)'
              ],
              borderColor: [
                'rgb(75, 192, 192)',
                'rgb(153, 102, 255)',
                'rgb(255, 159, 64)',
                'rgb(255, 99, 132)'
              ],
              borderWidth: 1
            }
          ]
        };
  
        const orderStatusData = {
          labels: ['Placed', 'Confirmed', 'Preparing', 'Ready', 'Captain Assigned', 'Out for Delivery', 'Delivered', 'Cancelled'],
          datasets: [
            {
              label: 'Order Status',
              data: [
                data.orderStatus.placed,
                data.orderStatus.confirmed,
                data.orderStatus.preparing,
                data.orderStatus.ready,
                data.orderStatus.captain,
                data.orderStatus.out_for_delivery,
                data.orderStatus.delivered,
                data.orderStatus.cancelled
              ],
              backgroundColor: [
                'rgba(54, 162, 235, 0.5)',
                'rgba(255, 205, 86, 0.5)',
                'rgba(251, 192, 45, 0.5)',
                'rgba(153, 102, 255, 0.5)',
                'rgba(255, 159, 64, 0.5)',
                'rgba(76, 175, 80, 0.5)',
                'rgba(46, 125, 50, 0.5)',
                'rgba(211, 47, 47, 0.5)'
              ],
              borderColor: [
                'rgb(54, 162, 235)',
                'rgb(255, 205, 86)',
                'rgb(251, 192, 45)',
                'rgb(153, 102, 255)',
                'rgb(255, 159, 64)',
                'rgb(76, 175, 80)',
                'rgb(46, 125, 50)',
                'rgb(211, 47, 47)'
              ],
              borderWidth: 1
            }
          ]
        };
  
        const deliveryData = {
          labels: ['On-time', 'Late', 'Cancelled'],
          datasets: [
            {
              label: 'Delivery Statistics',
              data: [
                data.deliveryStats.on_time,
                data.deliveryStats.late,
                data.deliveryStats.cancelled
              ],
              backgroundColor: [
                'rgba(75, 192, 192, 0.5)',
                'rgba(255, 205, 86, 0.5)',
                'rgba(255, 99, 132, 0.5)'
              ],
              borderColor: [
                'rgb(75, 192, 192)',
                'rgb(255, 205, 86)',
                'rgb(255, 99, 132)'
              ],
              borderWidth: 1
            }
          ]
        };
  
        const userGrowthData = {
          labels: data.userGrowth.map(item => item.month),
          datasets: [
            {
              label: 'New Users',
              data: data.userGrowth.map(item => item.users),
              backgroundColor: 'rgba(54, 162, 235, 0.5)',
              borderColor: 'rgba(54, 162, 235, 1)',
              borderWidth: 1
            }
          ]
        };
  
        // Create the charts
        new Chart(document.getElementById('orderTrendsChart'), {
          type: 'line',
          data: orderTrendsData,
          options: {
            scales: {
              y: {
                beginAtZero: true
              }
            }
          }
        });
  
        new Chart(document.getElementById('popularDishesChart'), {
          type: 'pie',
          data: popularDishesData,
          options: {
            responsive: true,
            maintainAspectRatio: false
          }
        });
  
        new Chart(document.getElementById('customerSatisfactionChart'), {
          type: 'doughnut',
          data: customerSatisfactionData,
          options: {
            responsive: true,
            maintainAspectRatio: false
          }
        });
  
        new Chart(document.getElementById('orderStatusChart'), {
          type: 'bar',
          data: orderStatusData,
          options: {
            scales: {
              y: {
                beginAtZero: true
              }
            }
          }
        });
  
        new Chart(document.getElementById('deliveryChart'), {
          type: 'bar',
          data: deliveryData,
          options: {
            scales: {
              y: {
                beginAtZero: true
              }
            }
          }
        });
  
        new Chart(document.getElementById('userGrowthChart'), {
          type: 'bar',
          data: userGrowthData,
          options: {
            scales: {
              y: {
                beginAtZero: true
              }
            }
          }
        });
      })
      .catch(error => console.error('Error fetching data:', error));
  });