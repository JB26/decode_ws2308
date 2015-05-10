function date_string_to_unix(d){
  return new Date(d.x.substring(0,4), d.x.substring(5,7), d.x.substring(8,10), d.x.substring(11,13), d.x.substring(14,16))
}
function new_graph(sensor){
  if (sensor == "temp"){
    sensor = "temp_out.temp_in"
    var id = "#temp svg"
  }
  opt = window.location.href.split("?")
  if (opt.length < 2){
    opt[1] = '';
  }
  $.getJSON( "/json_statistic/?" + opt[1], {sensor:sensor}, function(data) {
nv.addGraph(function() {
  var chart = nv.models.lineChart()
  
  chart.x(function(d) {return date_string_to_unix(d)})
  chart.xScale = d3.time.scale();
  chart.margin({left: 100, right: 100, bottom: 50});
  
  chart.xAxis
    .axisLabel('Datum')
    .tickFormat(function(d) { return d3.time.format("%Y-%m-%d %H:%M")(new Date(d)) })
    .tickPadding(10)
    ;

  chart.yAxis
    .axisLabel('Temperatur (°C)')
    .tickFormat(function(d) { return d3.format('.01f')(d) + '°C' })
    ;

  d3.select(id)
    .datum(data)
    .call(chart)
    ;

  nv.utils.windowResize(chart.update);
  return chart;
});
  })
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
}
