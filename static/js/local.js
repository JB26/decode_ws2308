var nIntervId;

$('.auto_reload').click(function(event) {
    $('.auto_reload').button('toggle');
    if ($(this).attr('id') == "auto_reload_off"){
        clearInterval(nIntervId);
    }else{
        reload_data();
        nIntervId =  setInterval(reload_data, 130000);
    }
})

function reload_data() {
    var sensors = ["temp_out.temp_in", "humidity_out.humidity_in", "wind_v.wind_d", "pressure_in.rain"],
        opt = "_type=seconds&number=130";
    for (sensor in sensors){
        sensor = sensors[sensor]
        $.getJSON( "/json_statistic/?" + opt, {sensor:sensor}, function(data) {
            var wind_text = '',
                chart_name = '';
            for (i in data){
                if (data[i].length > 1){
                    if (data[i][0] == "data_temp_out"){
                        $('#data_temp_out').text(data[i][data[i].length - 1] + ' °C');
                        chart_name = 'temp';
                    }else if (data[i][0] == "data_temp_in"){
                        $('#data_temp_in').text(data[i][data[i].length - 1] + ' °C');
                        chart_name = 'temp';
                    }else if (data[i][0] == "data_humidity_out"){
                        $('#data_humidity_out').text(data[i][data[i].length - 1] + ' %');
                        chart_name = 'humi';
                    }else if (data[i][0] == "data_humidity_in"){
                        $('#data_humidity_in').text(data[i][data[i].length - 1] + ' %');
                        chart_name = 'humi';
                    }else if (data[i][0] == "data_wind_v"){
                        wind_text = data[i][data[i].length - 1] + ' m/s; ' + wind_text;
                        chart_name = 'wind';
                    }else if (data[i][0] == "data_wind_d"){
                        wind_text = wind_text + data[i][data[i].length - 1] + '°';
                        chart_name = 'wind';
                    }else if (data[i][0] == "data_rain"){
                        $('#data_rain').text(data[i][data[i].length - 1] + ' ml');
                        chart_name = 'pres_rain';
                    }else if (data[i][0] == "data_pressure_in"){
                        $('#data_pressure_in').text(data[i][data[i].length - 1] + ' hPa');
                        chart_name = 'pres_rain';
                    }else if (data[i][0].slice(0,2) == "x_"){
                        $('#' + data[i][0]).text(data[i][data[i].length - 1]);
                    };
                };
            };
            if (wind_text != ''){
                $('#data_wind').text(wind_text);
            };
            if (chart_name != ''){
                chart[chart_name].flow({
                    columns: [
                        [data[0][0], data[0][data[0].length - 1]],
                        [data[1][0], data[1][data[1].length - 1]],
                        [data[2][0], data[2][data[2].length - 1]]
                    ]
                });
            };
        });
    };
}
