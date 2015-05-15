var nIntervId;

$('.auto_reload').click(function(event) {
    $('.auto_reload').button('toggle');
    if ($(this).attr('id') == "auto_reload_off"){
        clearInterval(nIntervId);
    }else{
        reload_data();
        nIntervId =  setInterval(reload_data, 125000);
    }
})

function reload_data() {
    var sensors = ["temp_out.temp_in", "humidity_out.humidity_in", "wind_v.wind_d", "pressure_in.rain", "wind_d_avg"],
        opt = "_type=hours&number=24";
    for (sensor in sensors){
        sensor = sensors[sensor]
        $.getJSON( "/json_statistic/?" + opt, {sensor:sensor}, function(data) {
            var ev_data = {min: data['min'], max: data['max']};
            data = data['data']
            var wind_text = '',
                chart_name = '';
            for (i in data){
                if (data[i][0] == "data_temp_out"){
                    $('#data_temp_out').text(data[i][1] + ' °C');
                    chart_name = 'temp';
                }else if (data[i][0] == "data_temp_in"){
                    $('#data_temp_in').text(data[i][1] + ' °C');
                    chart_name = 'temp';
                }else if (data[i][0] == "data_humidity_out"){
                    $('#data_humidity_out').text(data[i][1] + ' %');
                    chart_name = 'humi';
                }else if (data[i][0] == "data_humidity_in"){
                    $('#data_humidity_in').text(data[i][1] + ' %');
                    chart_name = 'humi';
                }else if (data[i][0] == "data_wind_v"){
                    wind_text = data[i][1] + ' m/s; ' + wind_text;
                    chart_name = 'wind';
                }else if (data[i][0] == "data_wind_d"){
                    wind_text = wind_text + data[i][1] + '°';
                    chart_name = 'wind';
                }else if (data[i][0] == "data_rain"){
                    $('#data_rain').text(data[i][1] + ' ml');
                    chart_name = 'pres_rain';
                }else if (data[i][0] == "data_pressure_in"){
                    $('#data_pressure_in').text(data[i][1] + ' hPa');
                    chart_name = 'pres_rain';
                }else if (data[i][0].slice(0,2) == "x_"){
                    $('#' + data[i][0]).text(data[i][1]);
                };
            };
            if (wind_text != ''){
                $('#data_wind').text(wind_text);
            };
            var evs = ['min', 'max'];
            for (ev in evs){
                ev=evs[ev]
                if (sensor == "temp_out.temp_in"){
                    $('#' + ev + '_data_temp_out').text(ev_data[ev]['temp_out']['value'] + ' °C');
                    $('#' + ev + '_data_temp_in').text(ev_data[ev]['temp_in']['value'] + ' °C');
                    $('#' + ev + '_x_temp_out').text(ev_data[ev]['temp_out']['date'] + ' °C');
                    $('#' + ev + '_x_temp_in').text(ev_data[ev]['temp_in']['date'] + ' °C')
                }else if (sensor == "humidity_out.humidity_in"){
                    $('#' + ev + '_data_humidity_out').text(ev_data[ev]['humidity_out']['value'] + ' %');
                    $('#' + ev + '_data_humidity_in').text(ev_data[ev]['humidity_in']['value'] + ' %');
                    $('#' + ev + '_x_humidity_out').text(ev_data[ev]['humidity_out']['date'] + ' %');
                    $('#' + ev + '_x_humidity_in').text(ev_data[ev]['humidity_in']['date'] + ' %')
                }else if (sensor == "pressure_in.rain"){
                    $('#' + ev + '_data_pressure_in').text(ev_data[ev]['pressure_in']['value'] + ' hPa');
                    $('#' + ev + '_x_pressure_in').text(ev_data[ev]['pressure_in']['date'] + ' hPa')
                }else if (sensor == "wind_v.wind_d"){
                    $('#' + ev + '_data_wind_v').text(ev_data[ev]['wind_v']['value'] + ' °C');
                    $('#' + ev + '_x_wind_v').text(ev_data[ev]['wind_v']['date'] + ' °C')
                };
            };
            if (chart_name != ''){
                chart[chart_name].load({
                    columns: data,
                });
            };
        });
    };
}
