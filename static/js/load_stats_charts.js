new_graph("temp", true, '_type=milliseconds&number=' + Date.now());
next = 'pres_rain';
$( document ).ajaxComplete(function() {
    if (next=='pres_rain'){
        new_graph("humi", true, '_type=milliseconds&number=' + Date.now());
        next = 'humi';
    }else if (next=='humi'){
        new_graph("wind", true, '_type=milliseconds&number=' + Date.now());
        next = 'wind';
    }else if (next=='wind'){
        new_graph("pres_rain", true, '_type=milliseconds&number=' + Date.now());
        next = 'wind_d_avg';
    }else if (next=='wind_d_avg'){
        new_graph("wind_d_avg", false, '_type=milliseconds&number=' + Date.now());
        next = 'None';
    };
});
