// dashboard_charts.js
// Uses global arrays: categoryData, dailyData, weeklyData, monthlyData.

document.addEventListener("DOMContentLoaded", function () {
    const currencySelect = document.getElementById("currency-switcher");

    const catLabels = categoryData.map(c => c.product__category);
    const catQty = categoryData.map(c => c.total_qty || 0);
    const catIncomeBase = categoryData.map(c => c.total_income || 0);

    const dailyLabels = dailyData.map(d => d.date);
    const dailyQty = dailyData.map(d => d.qty || 0);
    const dailyIncomeBase = dailyData.map(d => d.income || 0);

    const weeklyLabels = weeklyData.map(w => w.label);
    const weeklyQty = weeklyData.map(w => w.qty || 0);
    const weeklyIncomeBase = weeklyData.map(w => w.income || 0);

    const monthlyLabels = monthlyData.map(m => m.label);
    const monthlyQty = monthlyData.map(m => m.qty || 0);
    const monthlyIncomeBase = monthlyData.map(m => m.income || 0);

    function createChart(ctxId, labels, data, label, color) {
        const ctx = document.getElementById(ctxId);
        if (!ctx) return null;
        return new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: label,
                    data: data,
                    backgroundColor: color,
                }]
            },
            options: {
                responsive: true,
                animation: {
                    duration: 1200,
                    easing: 'easeOutQuart',
                },
                scales: {
                    y: { beginAtZero: true }
                }
            }
        });
    }

    const catQtyChart = createChart('catQtyChart', catLabels, catQty, 'Quantity', 'rgba(54, 162, 235, 0.7)');
    const catIncomeChart = createChart('catIncomeChart', catLabels, catIncomeBase, 'Income', 'rgba(255, 159, 64, 0.7)');

    const dailyQtyChart = createChart('dailyQtyChart', dailyLabels, dailyQty, 'Quantity', 'rgba(153, 102, 255, 0.7)');
    const dailyIncomeChart = createChart('dailyIncomeChart', dailyLabels, dailyIncomeBase, 'Income', 'rgba(75, 192, 192, 0.7)');

    const weeklyQtyChart = createChart('weeklyQtyChart', weeklyLabels, weeklyQty, 'Quantity', 'rgba(255, 206, 86, 0.7)');
    const weeklyIncomeChart = createChart('weeklyIncomeChart', weeklyLabels, weeklyIncomeBase, 'Income', 'rgba(255, 99, 132, 0.7)');

    const monthlyQtyChart = createChart('monthlyQtyChart', monthlyLabels, monthlyQty, 'Quantity', 'rgba(54, 162, 235, 0.7)');
    const monthlyIncomeChart = createChart('monthlyIncomeChart', monthlyLabels, monthlyIncomeBase, 'Income', 'rgba(255, 159, 64, 0.7)');

    function updateIncomeCharts() {
        if (!currencySelect) return;
        const rate = parseFloat(currencySelect.value || "1");

        if (catIncomeChart) {
            catIncomeChart.data.datasets[0].data = catIncomeBase.map(v => v * rate);
            catIncomeChart.update();
        }
        if (dailyIncomeChart) {
            dailyIncomeChart.data.datasets[0].data = dailyIncomeBase.map(v => v * rate);
            dailyIncomeChart.update();
        }
        if (weeklyIncomeChart) {
            weeklyIncomeChart.data.datasets[0].data = weeklyIncomeBase.map(v => v * rate);
            weeklyIncomeChart.update();
        }
        if (monthlyIncomeChart) {
            monthlyIncomeChart.data.datasets[0].data = monthlyIncomeBase.map(v => v * rate);
            monthlyIncomeChart.update();
        }
    }

    if (currencySelect) {
        currencySelect.addEventListener("change", updateIncomeCharts);
        updateIncomeCharts();
    }
});
