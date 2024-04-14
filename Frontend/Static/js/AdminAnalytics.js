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

  fetch('/admin/analytics/data')
    .then(response => response.json())
    .then(data => {
      const revenueData = {
        labels: data.RevenueDetails.map(item => item.revenue),
        datasets: [
          {
            label: 'Revenue',
            data: data.RevenueDetails.map(item => item.amount),
            backgroundColor: 'rgba(54, 162, 235, 0.5)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1,
            fill: true
          }
        ]
      };

      const averageOrderValueData = {
        labels: data.AverageOrderValue.map(item => item.month),
        datasets: [
          {
            label: 'Average Order Value',
            data: data.AverageOrderValue.map(item => item.average),
            backgroundColor: 'rgba(75, 192, 192, 0.5)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1
          }
        ]
      };

      const topRestaurantsData = {
        labels: data.TopRestaurants.map(item => item.name),
        datasets: [
          {
            label: 'Revenue',
            data: data.TopRestaurants.map(item => item.total_revenue),
            backgroundColor: 'rgba(255, 99, 132, 0.5)',
            borderColor: 'rgba(255, 99, 132, 1)',
            borderWidth: 1
          }
        ]
      };

      const peakOrderTimeData = {
        labels: data.PeakOrderTime.map(item => item.time),
        datasets: [
          {
            label: 'Peak Order Time',
            data: data.PeakOrderTime.map(item => item.orders),
            backgroundColor: 'rgba(255, 159, 64, 0.5)',
            borderColor: 'rgba(255, 159, 64, 1)',
            borderWidth: 1,
            fill: true
          }
        ]
      };

      const orderFrequencyData = {
        labels: data.OrderFrequency.map(item => item.month),
        datasets: [
          {
            label: 'Order Frequency',
            data: data.OrderFrequency.map(item => item.orders),
            backgroundColor: 'rgba(255, 99, 132, 0.5)',
            borderColor: 'rgb(255, 99, 132)',
            borderWidth: 1
          }
        ]
      };

      const repeatOrderRateData = {
        labels: ['Repeat Orders', 'New Orders'],
        datasets: [
          {
            label: 'Repeat Order Rate',
            data: [data.RepeatOrderRate.repeat_order_rate, 1 - data.RepeatOrderRate.repeat_order_rate],
            backgroundColor: [
              'rgba(75, 192, 192, 0.5)',
              'rgba(255, 99, 132, 0.5)'
            ],
            borderColor: [
              'rgb(75, 192, 192)',
              'rgb(255, 99, 132)'
            ],
            borderWidth: 1
          }
        ]
      };

      // Create the charts
      new Chart(document.getElementById('revenueChart'), {
        type: 'line',
        data: revenueData,
        options: {
          scales: {
            y: {
              beginAtZero: true,
              ticks: {
                callback: function(value) {
                  return '$' + value.toLocaleString();
                }
              }
            }
          }
        }
      });

      new Chart(document.getElementById('averageOrderValueChart'), {
        type: 'bar',
        data: averageOrderValueData,
        options: {
          scales: {
            y: {
              beginAtZero: true,
              ticks: {
                callback: function(value) {
                  return '$' + value.toLocaleString();
                }
              }
            }
          }
        }
      });

      new Chart(document.getElementById('topRestaurantsChart'), {
        type: 'bar',
        data: topRestaurantsData,
        options: {
          scales: {
            y: {
              beginAtZero: true,
              ticks: {
                callback: function(value) {
                  return '$' + value.toLocaleString();
                }
              }
            }
          }
        }
      });

      new Chart(document.getElementById('peakOrderTimeChart'), {
        type: 'line',
        data: peakOrderTimeData,
        options: {
          scales: {
            y: {
              beginAtZero: true,
              ticks: {
                callback: function(value) {
                  return value.toLocaleString();
                }
              }
            },
            x: {
              grid: {
                display: false
              }
            }
          }
        }
      });

      new Chart(document.getElementById('orderFrequencyChart'), {
        type: 'bar',
        data: orderFrequencyData,
        options: {
          scales: {
            y: {
              beginAtZero: true,
              ticks: {
                callback: function(value) {
                  return value.toLocaleString();
                }
              }
            }
          }
        }
      });

      new Chart(document.getElementById('repeatOrderRateChart'), {
        type: 'pie',
        data: repeatOrderRateData,
        options: {
          responsive: true,
          maintainAspectRatio: false
        }
      });
    })
    .catch(error => console.error('Error fetching data:', error));
});