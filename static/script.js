const ctx = document.getElementById("stockChart");

new Chart(ctx, {
    type: "line",
    data: {
        labels: chartLabels,
        datasets: [{
            label: "Stock Price",
            data: chartData,
            tension: 0.4,
            fill: true,
            borderColor: "#00ff84",
            backgroundColor: "rgba(0,255,132,0.1)",
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: {
                labels: { color: "white" }
            }
        },
        scales: {
            x: { ticks: { color: "white" } },
            y: { ticks: { color: "white" } }
        }
    }
});