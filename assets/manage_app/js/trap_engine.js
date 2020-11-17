var start_trap_engine_button = document.getElementById('id_start_trap_engine');
var stop_trap_engine_button = document.getElementById('id_stop_trap_engine');

function EngineCallMethod(button) {

    const csrf_token = getCookie('csrftoken');

    $.ajax({
        type: 'POST',
        url: ajax_trap_engine_url,
        data: {
            'button': button,
            'csrfmiddlewaretoken': csrf_token
        },
        dataType: 'json',
        success: function (data) {
            {
                console.log(data, button)
                var trap_buttons = document.getElementById('trap_buttons');

                if (data['traps_engine_running'] === false && button === 'start') {

                    start_trap_engine_button.parentNode.removeChild(start_trap_engine_button);

                    var stop_trap_engine_column = document.createElement('div');
                    stop_trap_engine_column.setAttribute('class', 'col');

                    stop_trap_engine_button = document.createElement('input');
                    stop_trap_engine_button.setAttribute('type', 'submit');
                    stop_trap_engine_button.setAttribute('id', 'id_stop_trap_engine');
                    stop_trap_engine_button.setAttribute('value', 'Stop Trap Engine');
                    stop_trap_engine_button.setAttribute('style', 'margin: 20px;position: absolute; right: 0;');
                    stop_trap_engine_button.setAttribute('class', 'btn btn-primary btn-customized');
                    stop_trap_engine_column.appendChild(stop_trap_engine_button)

                    stop_trap_engine_button.addEventListener('click', function () {
                        EngineCallMethod('stop');
                    });

                    trap_buttons.appendChild(stop_trap_engine_column)

                } else if (data['traps_engine_running'] === true && button === 'stop') {
                    stop_trap_engine_button.parentNode.removeChild(stop_trap_engine_button);

                    var start_trap_engine_column = document.createElement('div');

                    start_trap_engine_column.setAttribute('class', 'col');
                    start_trap_engine_button = document.createElement('input');
                    start_trap_engine_button.setAttribute('type', 'submit');
                    start_trap_engine_button.setAttribute('id', 'id_start_trap_engine');
                    start_trap_engine_button.setAttribute('value', 'Start Trap Engine');
                    start_trap_engine_button.setAttribute('style', 'margin: 20px;position: absolute; right: 0;');
                    start_trap_engine_button.setAttribute('class', 'btn btn-primary btn-customized');

                    start_trap_engine_button.addEventListener('click', function () {
                        EngineCallMethod('start');
                    });

                    start_trap_engine_column.appendChild(start_trap_engine_button)

                    trap_buttons.appendChild(start_trap_engine_column)

                }
            }
        }
    })
}

$("#id_start_trap_engine").click(function () {
    EngineCallMethod('start')
})

$("#id_stop_trap_engine").click(function () {
    EngineCallMethod('stop')
})