from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import ConfigParameters
from .forms import ConfigParametersForm
from .models import AvailableDevices
from .backend.static import discovery_protocol, device_os
from .backend.initial_config import ConnectionManager
from .backend.parse_model import parse_config
from .backend.general_functions import ping_all


# Create your views here.
@login_required(redirect_field_name='')
def config_network_view(request):
    form = ConfigParametersForm(request.POST or None)
    user = User.objects.filter(username=request.user)[0]
    print(request.POST)

    if request.method == 'POST':
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()

    if 'delete_all' in request.POST:
        AvailableDevices.objects.all().delete()
        ConfigParameters.objects.all().delete()
        form = ConfigParametersForm()

    elif 'run_config' in request.POST:
        available_hosts = list()
        form = ConfigParametersForm()
        object_id = request.POST.get('id')

        config, login_params = parse_config(object_id)

        for host in AvailableDevices.objects.all():
            available_hosts.append(host.network_address)

        initial_config = ConnectionManager(config, login_params, available_hosts)

        commands = ['lldp run', 'int lo0', 'ip address 1.1.1.1 255.255.255.255']
        cf_output = initial_config.connect_and_configure_multiple(commands)

        if cf_output is None:
            error_logging_message = 'Invalid Logging Credentials!'

    elif 'available_hosts' in request.POST:
        object_id = ConfigParameters.objects.first().id
        config, _ = parse_config(object_id)

        available_hosts = ping_all(config)

        for host in available_hosts:
            new_host = AvailableDevices(user=user, network_address=host)
            new_host.save()

    context = {
        'parameters_list': ConfigParameters.objects.filter(user=request.user),
        'available_hosts': AvailableDevices.objects.filter(user=request.user),
        'form': form,
        'protocol': discovery_protocol,
        'device_os': device_os.keys(),
        'error_logging_message': error_logging_message
    }

    return render(request, 'config_network.html', context)
