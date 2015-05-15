new_graph("temp", false, '_type=hours&number=24');
next = 'pres_rain';
$( document ).ajaxComplete(function() {
    if (next=='pres_rain'){
        new_graph("pres_rain", false, '_type=hours&number=24');
        next = 'humi';
    }else if (next=='humi'){
        new_graph("humi", false, '_type=hours&number=24');
        next = 'wind';
    }else if (next=='wind'){
        new_graph("wind", false, '_type=hours&number=24');
        next = 'wind_d_avg';
    }else if (next=='wind_d_avg'){
        new_graph("wind_d_avg", false, '_type=hours&number=24');
        next = 'None';
    }
});
