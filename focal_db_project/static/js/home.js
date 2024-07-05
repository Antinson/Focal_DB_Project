import { createChart, createChartUser } from './graphs.js'





document.addEventListener('DOMContentLoaded', () => {
    createChart();
    Chart.register(ChartDataLabels);
});