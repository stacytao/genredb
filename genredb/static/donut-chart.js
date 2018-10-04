const COLORS = [
    '#f0ad4e',
    '#4582EC',
    '#02B875',
    '#ced4da',
    '#e83e8c',
    '#17a2b8',
    '#6f42c1',
    '#fd7e14',
    '#868e96',
    '#20c997',
    '#6610f2',
    '#d9534f',
    '#212529'
]

let ctx = $("#donutChart");
let chartData = ctx.data().value;

console.log(chartData);

let distinctGenreCount = chartData.genres.length;

console.log(chartData.genres);
console.log(chartData.quantities);
console.log(chartData.genres.length === chartData.quantities.length);

let donutChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
        labels: chartData.genres,
        datasets: [{
            label: '# of Votes',
            data: chartData.quantities,
            backgroundColor: COLORS.slice(0, distinctGenreCount)
        }]
    }
});