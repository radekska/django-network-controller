let socket = null
let term = new Terminal({
    cursorBlink: 'block',
})
term.resize(117, 24)


var ssh_buttons = document.getElementById('id_session_buttons')

function SSHCallMethod(loc, button) {
    const csrf_token = getCookie('csrftoken');
    const regex = /\d.*/
    const device_id = loc.search.match(regex)[0]
    console.log(device_id)
    $.ajax({
        type: 'POST',
        url: ajax_ssh_url,
        data: {
            'device_id': device_id,
            'button': button,
            'csrfmiddlewaretoken': csrf_token
        },
        dataType: 'json',
        success: function (data) {
            console.log(data)
            var start_ssh_session = document.getElementById('id_ssh_session_start');
            var stop_ssh_session = document.getElementById('id_ssh_session_stop');

            if (button === 'start') {

                if (loc.search !== '') {
                    var ws_start = 'ws://'
                    if (loc.proto === 'https:') {
                        ws_start = 'wss://'
                    }
                    var ws_endpoint = ws_start + loc.host + loc.pathname + loc.search
                    socket = new WebSocket(ws_endpoint)

                    let char_buffer = ''
                    var stdin_allowed = true
                    var response_data = null
                    var prompt = null

                    socket.onmessage = function (e) {
                        console.log("message", e)
                        response_data = JSON.parse(e.data)
                        var response = response_data.response
                        prompt = response_data.current_prompt
                        term.write('\r'+response)
                    }

                    socket.onerror = function (e) {
                        console.log("message", e)
                    }
                    socket.onclose = function (e) {
                        stdin_allowed = false
                        console.log(e)
                    }

                    socket.onopen = function (e) {
                        stdin_allowed = true
                        console.log("message", e)

                        term.onKey(data => {
                                if (stdin_allowed) {
                                    if (data.domEvent.key === 'Backspace') {
                                        if (term.buffer.active.cursorX > prompt.length) {
                                            char_buffer = char_buffer.slice(0, -1)
                                            term.write("\b \b")
                                        }
                                    } else if (data.domEvent.key === 'Enter') {
                                        char_buffer += '\n'
                                        if (char_buffer === 'exit\n') {
                                            term.write('\r\nClosing SSH session...')
                                            socket.send(char_buffer)
                                            socket.close()
                                        } else if (char_buffer === 'clear\n') {
                                            term.clear()
                                        } else {
                                            socket.send(char_buffer)

                                        }
                                        term.write('\r')
                                        char_buffer = ''
                                    } else {
                                        if (data.domEvent.key !== 'ArrowDown' && data.domEvent.key !== 'ArrowUp') {
                                            term.write(data.key)
                                            if (data.domEvent.key !== 'ArrowLeft' && data.domEvent.key !== 'ArrowRight') {
                                                char_buffer += data.key
                                            }
                                        }

                                    }
                                }

                            }
                        )
                        ;
                    }


                    term.open(document.getElementById('terminal'));
                }
                start_ssh_session.parentNode.removeChild(start_ssh_session)

                var stop_ssh_session_column = document.createElement('div');
                stop_ssh_session_column.setAttribute('class', 'col');


                stop_ssh_session = document.createElement('input');
                stop_ssh_session.setAttribute('type', 'submit');
                stop_ssh_session.setAttribute('id', 'id_ssh_session_stop')
                stop_ssh_session.setAttribute('value', 'Stop SSH Session')
                stop_ssh_session.setAttribute('style', 'margin: 20px;position: absolute; right: 0;');
                stop_ssh_session.setAttribute('class', 'btn btn-primary btn-customized');
                stop_ssh_session_column.appendChild(stop_ssh_session)

                stop_ssh_session.addEventListener('click', function () {
                    SSHCallMethod(loc, 'stop')
                })

                ssh_buttons.appendChild(stop_ssh_session_column)

            } else if (button === 'stop') {
                stop_ssh_session.parentNode.removeChild(stop_ssh_session)

                var start_ssh_session_column = document.createElement('div');
                start_ssh_session_column.setAttribute('class', 'col');


                start_ssh_session = document.createElement('input');
                start_ssh_session.setAttribute('type', 'submit');
                start_ssh_session.setAttribute('id', 'id_ssh_session_start')
                start_ssh_session.setAttribute('value', 'Start SSH Session')
                start_ssh_session.setAttribute('style', 'margin: 20px;position: absolute; right: 0;');
                start_ssh_session.setAttribute('class', 'btn btn-primary btn-customized');
                start_ssh_session_column.appendChild(start_ssh_session)

                start_ssh_session.addEventListener('click', function () {
                    SSHCallMethod(loc, 'start')
                })

                ssh_buttons.appendChild(start_ssh_session_column)
                term.write('\r\nClosing SSH session...')
                socket.close()
            }
        }

    })

}

$('#id_ssh_session_start').click(function () {
    var loc = window.location
    SSHCallMethod(loc, 'start')
})

$('#id_ssh_session_stop').click(function () {
    var loc = window.location
    SSHCallMethod(loc, 'stop')
})