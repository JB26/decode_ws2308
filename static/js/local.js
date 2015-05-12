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
    var sensor = "temp_out.temp_in.humidity_out.humidity_in.wind_v.wind_d.pressure_in.rain",
        opt = "_type=seconds&number=130";
    $.getJSON( "/json_statistic/?" + opt, {sensor:sensor}, function(data) {
        var data_dict = new Object(),
            wind_text = '';
        for (i in data){
            if (data[i].length > 1){
                if (data[i][0] == "data_temp_out"){
                    $('#data_temp_out').text(data[i][data[i].length - 1] + ' °C');
                }else if (data[i][0] == "data_temp_in"){
                    $('#data_temp_in').text(data[i][data[i].length - 1] + ' °C');
                }else if (data[i][0] == "data_humidity_out"){
                    $('#data_humidity_out').text(data[i][data[i].length - 1] + ' %');
                }else if (data[i][0] == "data_humidity_in"){
                    $('#data_humidity_in').text(data[i][data[i].length - 1] + ' %');
                }else if (data[i][0] == "data_wind_v"){
                    wind_text = data[i][data[i].length - 1] + ' m/s; ' + wind_text;
                }else if (data[i][0] == "data_wind_d"){
                    wind_text = wind_text + data[i][data[i].length - 1] + '°';
                }else if (data[i][0] == "data_rain"){
                    $('#data_rain').text(data[i][data[i].length - 1] + ' ml');
                }else if (data[i][0] == "data_pressure_in"){
                    $('#data_pressure_in').text(data[i][data[i].length - 1] + ' hPa');
                }else if (data[i][0].slice(0,2) == "x_"){
                    $('#' + data[i][0]).text(data[i][data[i].length - 1]);
                }
            }
        }
        if (wind_text != ''){
            $('#data_wind').text(wind_text);
        }
    })
}
