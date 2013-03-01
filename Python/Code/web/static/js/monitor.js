$(document).ready(function() {
    min_date = null;
    data = eval($("#data").html());
    i = 0;
    while (i < data.length) {
        date = new Date(data[i][0].split(" ")[0]);
        if (min_date == null) {
            min_date = date;
        } else {
            if (date < min_date) {
                min_date = date;
            }
        }
        i++;
    }
    var plot = $.jqplot("chart", [data], {
        axes: {
            xaxis: {
                renderer: $.jqplot.DateAxisRenderer,
                min: min_date.toLocaleFormat("%b %e, %Y"),
                tickInterval: '15 days',
                tickOptions: {
                    formatString: '%b %#d, %y',
                    fontSize: '10pt'
                }
            },
            yaxis: {
                min: 0,
                max: 100
            }
        },
        cursor: {
            show: true,
            zoom: true,
            showTooltip: false
        },
        series: [{
            color: 'red',
            lineWidth: 1,
            neighborThreshold: -1,
            showMarker: true
        }]
    });
    $("#reset-button").click(function() { plot.resetZoom(); });
});
