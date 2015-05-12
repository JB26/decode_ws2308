window.onload = function(){
    new_graph("temp", true, '_type=milliseconds&number=' + Date.now());
    new_graph("humi", true, '_type=milliseconds&number=' + Date.now());
    new_graph("wind", true, '_type=milliseconds&number=' + Date.now());
    new_graph("pres_rain", true, '_type=milliseconds&number=' + Date.now());
    new_graph("wind_d_avg", false, '_type=milliseconds&number=' + Date.now());
}
