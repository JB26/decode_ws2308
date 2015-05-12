function new_graph(chart_name, show_subchart, range){
    if (chart_name == "temp"){
        var sensor = "temp_out.temp_in"
        var id = "#temp",
            x_coord = {
                'data_temp_out' : 'x_temp_out',
                'data_temp_in' : 'x_temp_in'
            },
            y_label = 'Temperatur',
            y_unit = '°C',
            data_names = {
                data_temp_out: 'Aussen',
                data_temp_in: 'Innen'
            },
            two_y_axes = false;
    }else if (chart_name == "humi"){
        var sensor = "humidity_out.humidity_in"
        var id = "#humi",
            x_coord = {
                'data_humidity_out' : 'x_humidity_out',
                'data_humidity_in' : 'x_humidity_in'
            },
            y_label = 'Luftfeuchtigkeit',
            y_unit = '%',
            data_names = {
                data_humidity_out: 'Aussen',
                data_humidity_in: 'Innen'
            },
            two_y_axes = false;
    }else if (chart_name == "wind"){
        var sensor = "wind_v.wind_d"
        var id = "#wind",
            x_coord = {
                'data_wind_v' : 'x_wind_v',
                'data_wind_d' : 'x_wind_d'
            },
            y_label = 'Windgeschwindigkeit',
            y2_label = 'Windrichtung',
            y_unit = 'm/s',
            y2_unit = '°',
            data_names = {
                data_wind_v: 'Geschwindigkeit',
                data_wind_d: 'Richtung'
            },
            two_y_axes = true,
            y_axes = {
                data_wind_v: 'y',
                data_wind_d: 'y2'
            };
    }else if (chart_name == "pres_rain"){
        var sensor = "pressure_in.rain"
        var id = "#pres_rain",
            x_coord = {
                'data_pressure_in' : 'x_pressure_in',
                'data_rain' : 'x_rain'
            },
            y_label = 'Luftdruck',
            y2_label = 'Regen',
            y_unit = 'hPa',
            y2_unit = 'ml',
            data_names = {
                data_pressure_in: 'Luftdruck',
                data_rain: 'Regen'
            },
            two_y_axes = true,
            y_axes = {
                data_pressure_in: 'y',
                data_rain: 'y2'
            };
    }
    var opt = window.location.href.split("?");
    if (opt.length < 2){
        opt[1] = range;
    };
    var tickMultiFormat = d3.time.format.multi([
        ["%H:%M", function(d) { return d.getMinutes(); }], // not the beginning of the hour
        ["%H", function(d) { return d.getHours(); }], // not midnight
        ["%d.%m", function(d) { return d.getDate() != 1; }], // not the first of the month
        ["%d.%m", function(d) { return d.getMonth(); }], // not Jan 1st
        ["%Y", function() { return true; }]
    ]);
    chart = new Object(); //Global
    $.getJSON( "/json_statistic/?" + opt[1], {sensor:sensor}, function(data) {
        var chart_settings = {
            bindto: id,
            padding: {
                bottom: 5,
            },
            data: {
                xs: x_coord,
                xFormat: '%Y-%m-%d %H:%M',
                columns: data,
                type: 'spline',
                types: {
                    data_rain: 'bar'
                },
                names: data_names
            },
            subchart: {
                show: show_subchart
            },
            grid: {
                x: {
                    show: true
                },
                y: {
                    show: true
                }
            },
            point: {
                show: false
            },
            axis: {
                x: {
                    type: 'timeseries',
                    tick: {
                        fit : false,
                        format: function (d) { return tickMultiFormat(new Date(d)); }
                    },
                    label: {
                        text: 'Uhrzeit',
                        position: 'outer-center'
                    }
                },
                y: {
                    tick: {
                        format: function (d) { return d + y_unit; }
                    },
                    label: {
                        text: y_label,
                        position: 'outer-middle'
                    }
                }
            },
            tooltip: {
                format: {
                    title: function(d) { return d3.time.format('%Y-%m-%d %H:%M')(new Date(d)) }
                }
            }
        };
        if (two_y_axes){
            chart_settings.data.axes = y_axes;
            chart_settings.axis.y2 = {
                show: true,
                tick: {
                    format: function (d) { return d + y2_unit; }
                },
                label: {
                    text: y2_label,
                    position: 'outer-middle'
                }
            }
        };
        chart[chart_name] = c3.generate(chart_settings)
    });
};

$('.zoom').click(function(event) {
    var new_range = [],
        chart_name = $(this).attr('id').split("_")[1],
        z = chart[chart_name].zoom();
    for (i = 0; i < 2; i++) {
        new_range[i] = z[i].getFullYear() + '-' + pad(z[i].getMonth() + 1) +
            '-' + pad(z[i].getDate()) + 'T' + pad(z[i].getHours()) + ':' +
            pad(z[i].getMinutes())
    };
    window.location.href = "/stats?start_date=" + new_range[0] +
        "&end_date=" + new_range[1]
});

function pad(number) {
    if (number < 10) {
        return '0' + number;
    }
        return number;
}
