$(document).ready(function() {
    data = $.map(eval($("#data").html()), function(d) {
        return [[(new Date(d[0])).getTime(), d[1]]];
    });
    
    window.chart = new Highcharts.StockChart({
        chart: {
            renderTo: "chart"
        },
        rangeSelector: {
            selected: 1
        },
        title: {
            text: "Depression Rate v/s Time"
        },
        tooltip: {
            style: {
                width: '200px'
            },
            valueDecimals: 2
        },
        yAxis: {
            title: {
                text: "% population depressed"
            }
        },
        series: [{
            name: "%",
            data: data,
            id: 'dataseries'
        }]
    });
});
