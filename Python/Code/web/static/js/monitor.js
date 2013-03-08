$(document).ready(function() {
    data = $.map(eval($("#data").html()), function(e) {
        return [[(new Date(e[0])).getTime(), e[1]]];
    });
    
    labels = $.map($.map(eval($("#labelled_tweets").html()), function(e) {
        return [[(new Date(e[0])).getTime(), e[1]]];
    }), function(e) {
        return { x: e[0], title: "T", text: e[1] };
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
        },
        {
            type: 'flags',
            data: labels,
            onSeries: 'dataseries',
            shape: 'circlepin',
            width: 16
        }]
    });
});
