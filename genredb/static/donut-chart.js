const COLORS = [
    '#4582EC', // litera blue
    '#02B875', // litera green
    '#F0AD4E', // litera yellow
    '#17A2B8', // litera teal
    '#D9534F', // litera red
    '#FFE27A', // light yellow
    '#60E9FF', // light blue
    '#F47C27', // orange
    '#184F87', // dark blue
    '#A32356', // magenta
    '#491E70', // purple
    '#FF608D', // pink
    '#85FFC7', // mint green
    '#FCFC62', // lemon yellow
    '#63D471', // lime green
    '#AA86E0', // light purple
    '#187243', // dark green
    '#7C3F0C', // brown
    '#6B1139', // dark raspberry
    '#757F06', // olive
]

let ctx = $("#donutChart");
let chartData = ctx.data().value;

let distinctGenreCount = chartData.genres.length;

let donutChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
        labels: chartData.genres,
        datasets: [{
            label: 'Number of Movies',
            data: chartData.quantities,
            backgroundColor: COLORS.slice(0, distinctGenreCount)
        }]
    }
});