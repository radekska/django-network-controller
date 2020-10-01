from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import ConfigParameters, SNMPConfigParameters
from .forms import ConfigParametersForm, SNMPConfigParametersForm
from .models import AvailableDevices
from .backend.static import discovery_protocol, device_os
from .backend.initial_config import ConnectionManager
from .backend.parse_model import parse_config
from .backend.general_functions import ping_all


# Create your views here.
@login_required(redirect_field_name='')
def config_network_view(request):
    print(request.POST)

    error_logging_message = None
    config_parameters_form = None
    snmp_config_parameters_form = None

    user = User.objects.filter(username=request.user)[0]

    if 'add_initial_config' in request.POST:
        config_parameters_form = ConfigParametersForm(request.POST or None)
        if config_parameters_form.is_valid():
            instance = config_parameters_form.save(commit=False)
            instance.user = request.user
            instance.save()

    if 'add_snmp_config' in request.POST:
        snmp_config_parameters_form = SNMPConfigParametersForm(request.POST or None)
        if snmp_config_parameters_form.is_valid():
            instance = snmp_config_parameters_form.save(commit=False)
            instance.user = request.user
            instance.save()

    elif 'initial_delete_all' in request.POST:
        AvailableDevices.objects.all().delete()
        ConfigParameters.objects.all().delete()
        config_parameters_form = ConfigParametersForm()

    elif 'snmp_delete_all' in request.POST:
        SNMPConfigParameters.objects.all().delete()
        snmp_config_parameters_form = SNMPConfigParametersForm()

    elif 'run_config' in request.POST:
        available_hosts = list()
        config_parameters_form = ConfigParametersForm()
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
        AvailableDevices.objects.all().delete()
        object_id = ConfigParameters.objects.first().id
        config, _ = parse_config(object_id)

        available_hosts = ping_all(config)

        for host in available_hosts:
            new_host = AvailableDevices(user=user, network_address=host)
            new_host.save()

    context = {
        'initial_config_parameters_list': ConfigParameters.objects.filter(user=request.user),
        'snmp_config_parameters_list': SNMPConfigParameters.objects.filter(user=request.user),
        'available_hosts': AvailableDevices.objects.filter(user=request.user),
        'config_parameters_form': config_parameters_form,
        'snmp_config_parameters_form': snmp_config_parameters_form,
        'protocol': discovery_protocol,
        'device_os': device_os.keys(),
        'error_logging_message': error_logging_message
    }

    return render(request, 'config_network.html', context)
