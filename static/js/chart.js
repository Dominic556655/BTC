const ctx = document.getElementById('btcChart').getContext('2d');
const btcChart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: dates,
    datasets: [{
      label: 'BTC/USD (Last 7 days)',
      data: prices,
      borderColor: 'rgba(75, 192, 192, 1)',
      tension: 0.1,
    }]
  },
  options: {
    scales: {
      y: {
        beginAtZero: false
      }
    }
  }
});
