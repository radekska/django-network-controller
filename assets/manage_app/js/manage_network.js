function AddNavTags() {
    var first_nav_tag = document.getElementById('id_page_first');
    var previous_nav_tag = document.getElementById('id_page_previous');

    first_nav_tag.innerHTML = '&laquo; first ';
    previous_nav_tag.innerText = 'previous';

    var all_links = document.getElementById('links')
    all_links.insertBefore(previous_nav_tag, all_links.firstChild)
    all_links.insertBefore(first_nav_tag, all_links.firstChild)
}


function CallMethod(page_number, call_type) {
    $.ajax({
        type: 'GET',
        url: ajax_trap_view_url,
        data: {
            'page_number': page_number
        },
        dataType: 'json',
        success: function (data) {
            var content = '';
            for (var i = 0; i < data['trap_json_data'].length; i++) {
                content += `<tr>
                                                                            <th scope="row">${data['trap_json_data'][i]['pk']}</th>
                                                                            <td style="width: 160px">${data['trap_json_data'][i]['fields']['trap_date']}</td>
                                                                            <td>${data['trap_json_data'][i]['fields']['trap_address']}</td>
                                                                            <td>${data['trap_json_data'][i]['fields']['trap_port']}</td>
                                                                            <td>${data['trap_json_data'][i]['fields']['trap_string_data']}</td>
                                                                            </tr>`
            }
            $("#trap_table tbody").html(content);

            var first = document.getElementById('id_page_first');
            var previous = document.getElementById('id_page_previous');
            var last = document.getElementById('id_page_last');
            var next = document.getElementById('id_page_next');
            var page_counter = '';
            var page_number = '';

            if (call_type === 'first') {
                first.innerHTML = '';
                previous.innerText = '';
                next.innerText = 'next';
                last.innerHTML = 'last &raquo';

                page_counter = 'Page 1 of ' + last.getAttribute('data');
                document.getElementById('id_page_next').setAttribute('data', '2')


            } else if (call_type === 'previous') {
                page_number = data['current_page'];
                var next_page_number = (parseInt(page_number) + 1).toString()
                page_counter = 'Page ' + page_number + ' of ' + last.getAttribute('data');

                document.getElementById('id_page_next').setAttribute('data', next_page_number)
                if (page_number < data['last_page']) {
                    next.innerText = 'next';
                    last.innerHTML = 'last &raquo';
                }

                if (data['current_page'] === '1') {
                    first.innerHTML = '';
                    previous.innerText = '';
                }


            } else if (call_type === 'last') {
                first.innerHTML = '&laquo first ';
                previous.innerText = 'previous';
                next.innerText = '';
                last.innerText = '';
                page_counter = 'Page ' + last.getAttribute('data') + ' of ' + last.getAttribute('data');
                document.getElementById('id_page_next').setAttribute('data', (parseInt(last.getAttribute('data')) + 1).toString())

            } else if (call_type === 'next') {
                var current_page = data['current_page']
                page_number = (parseInt(data['current_page']) + 1).toString();
                page_counter = 'Page ' + current_page + ' of ' + last.getAttribute('data');

                document.getElementById('id_page_next').setAttribute('data', page_number)

                if (page_number > data['last_page']) {
                    next.innerText = '';
                    last.innerText = '';
                }

                if (data['current_page'] !== 1) {
                    first.innerHTML = '&laquo first ';
                    previous.innerText = 'previous';
                }

            }
            document.getElementById('id_page_current').innerText = page_counter
        }
    });
}

var nav_tags_added = false;

$("#id_page_first").click(function () {
    nav_tags_added = false;
    CallMethod('1', 'first')
})

$("#id_page_previous").click(function () {
    var page_number = document.getElementById('id_page_next').getAttribute('data');
    page_number = (parseInt(page_number) - 2).toString();
    if (page_number < 1) {
        page_number = 1;
    }
    CallMethod(page_number, 'previous');
})

$("#id_page_next").click(function () {
    var page_number = $(this).attr('data');

    if (!nav_tags_added) {
        nav_tags_added = true;
        AddNavTags();
    }

    CallMethod(page_number, 'next');

})

$("#id_page_last").click(function () {
    var last_page = $(this).attr('data')

    if (!nav_tags_added) {
        nav_tags_added = true;
        AddNavTags();
    }
    CallMethod(last_page, 'last');
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


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
                console.log(data)
                var trap_buttons = document.getElementById('trap_buttons');
                if (data['traps_engine_running'] === false) {

                    var start_trap_engine_button = document.getElementById('id_start_trap_engine');
                    start_trap_engine_button.parentNode.removeChild(start_trap_engine_button);

                    var stop_trap_engine_column = document.createElement('div');
                    stop_trap_engine_column.setAttribute('class', 'col');

                    var stop_trap_engine_button = document.createElement('input');
                    stop_trap_engine_button.setAttribute('type', 'submit');
                    stop_trap_engine_button.setAttribute('id', 'id_stop_trap_engine');
                    stop_trap_engine_button.setAttribute('value', 'Stop Trap Engine');
                    stop_trap_engine_button.setAttribute('style', 'margin: 20px');
                    stop_trap_engine_button.setAttribute('class', 'btn btn-primary btn-customized');
                    stop_trap_engine_column.appendChild(stop_trap_engine_button)

                    trap_buttons.appendChild(stop_trap_engine_column)

                } else if (data['traps_engine_running'] === true){

                }
            }
        }
    })
}

$("#id_start_trap_engine").click(function () {
    EngineCallMethod('start')
})

$("#id_stop_trap_engine").click(function () {
    console.log(document.getElementById('id_stop_trap_engine').value)
    EngineCallMethod('stop')
})