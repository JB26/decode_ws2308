function date_string_to_unix(d){
    var date = d.x
    return new Date(date.substring(0,4), date.substring(5,7), date.substring(8,10), date.substring(11,13), date.substring(14,16))
}

var wur = "hello"

function new_graph(sensor){
    if (sensor == "temp"){
        sensor = "temp_out.temp_in"
        var id = "#temp svg"
    };
    var opt = window.location.href.split("?");
    if (opt.length < 2){
        opt[1] = '';
    };
    $.getJSON( "/json_statistic/?" + opt[1], {sensor:sensor}, function(data) {
        
        var tickMultiFormat = d3.time.format.multi([
            ["%-H:%M", function(d) { return d.getMinutes(); }], // not the beginning of the hour
            ["%-H", function(d) { return d.getHours(); }], // not midnight
            ["%b %-d", function(d) { return d.getDate() != 1; }], // not the first of the month
            ["%b %-d", function(d) { return d.getMonth(); }], // not Jan 1st
            ["%Y", function() { return true; }]
        ]);
        nv.addGraph(function() {
        chart = nv.models.lineWithFocusChart()
        
        //chart.xScale = d3.time.scale();
        chart.margin({left: 100, right: 100, bottom: 50});
        chart.brushExtent([1431323000, 1431329000])
        chart.useInteractiveGuideline(true)
        
        chart.xAxis
            .axisLabel('Datum')
            .tickFormat(function (d) { return tickMultiFormat(new Date(d*1000)); })
            .tickPadding(10)
            //.ticks(4)
            ;
    
        chart.yAxis
            .axisLabel('Temperatur (°C)')
            .tickFormat(function(d) { return d3.format('.01f')(d) + '°C' })
            ;

        chart.x2Axis
            .axisLabel('Datum')
            .tickFormat(function(d) { return d3.time.format("%Y-%m-%d %H:%M")(new Date(d*1000)) })
            .tickPadding(10)
            .ticks(2)
            ;
    
        chart.y2Axis
            .tickFormat(function(d) { return d3.format('.01f')(d) + '°C' })
            ;
    
        d3.select(id)
            .datum(data)
            .call(chart)
            ;
    
        nv.utils.windowResize(chart.update);
        });
    });
};

window.onload = function(){
    new_graph("temp");
    //new_graph("humidity_out");
    //new_graph("wind_v");
    //new_graph("wind_d");
    //new_graph("rain");
    //new_graph("temp_in");
    //new_graph("humidity_in");
    //new_graph("pressure_in");
    //alert(d3.select("#temp").chart.brushExtent());
}
