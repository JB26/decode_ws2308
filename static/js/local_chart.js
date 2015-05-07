function new_graph(sensor){
  $.getJSON( "/json_statistic/", {sensor:sensor}, function(data) {
    var barChartData = {
      labels : data["labels"],
      datasets : [
        {
          fillColor : "rgba(151,187,205,0.5)",
          strokeColor : "rgba(151,187,205,0.8)",
          pointHighlightFill : "rgba(151,187,205,0.75)",
          pointHighlightStroke : "rgba(151,187,205,1)",
          data : data["values"]
        }
      ]
    };
    var ctx = $("#" + sensor).get(0).getContext("2d");
    var settings = {
      responsive : true,
      animation: false,
      pointDot : false,
      pointHitDetectionRadius : 5
    };
    if (sensor == "humidity_out"){
      settings.scaleOverride = true;
      settings.scaleSteps = 10;
      settings.scaleStepWidth = 10;
      settingsscaleStartValue = 0;
    }else if (sensor == "wind_d"){
      settings.scaleOverride = true;
      settings.scaleSteps = 6;
      settings.scaleStepWidth = 60;
      settingsscaleStartValue = 0;
    };
    window[sensor] = new Chart(ctx).Line(barChartData, settings);
  })
};

window.onload = function(){
  new_graph("temp_out");
  new_graph("humidity_out");
  new_graph("wind_v");
  new_graph("wind_d");
  new_graph("rain");
  new_graph("temp_in");
  new_graph("humidity_in");
  new_graph("pressure_in");
}
