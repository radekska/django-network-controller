from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import ConfigParameters, SNMPConfigParameters
from .forms import ConfigParametersForm, SNMPConfigParametersForm
from .models import AvailableDevices
from .backend.static import discovery_protocol, device_os
from .backend.initial_config import ConnectionManager
from .backend.parse_model import parse_initial_config, parse_snmp_config
from .backend.general_functions import ping_all


# Create your views here.
@login_required(redirect_field_name='')
def config_network_view(request):
    success_status_message = None
    warning_status_message = None
    error_status_message = None
    config_parameters_form = None
    snmp_config_parameters_form = None

    user = User.objects.filter(username=request.user)[0]

    print(request.POST)

    if 'add_access_config' in request.POST:
        config_parameters_form = ConfigParametersForm(request.POST or None)
        if config_parameters_form.is_valid():
            instance = config_parameters_form.save(commit=False)
            instance.user = request.user
            instance.save()

            success_status_message = 'Access Configuration Added Successfully!'

    if 'add_snmp_config' in request.POST:
        snmp_config_parameters_form = SNMPConfigParametersForm(request.POST or None)
        if snmp_config_parameters_form.is_valid():
            instance = snmp_config_parameters_form.save(commit=False)
            instance.user = request.user
            instance.save()

            success_status_message = 'SNMPv3 Configuration Added Successfully!'

    elif 'access_delete_all' in request.POST:
        AvailableDevices.objects.all().delete()
        ConfigParameters.objects.all().delete()
        config_parameters_form = ConfigParametersForm()

        warning_status_message = 'Removed All Access Configurations...'

    elif 'snmp_delete_all' in request.POST:
        SNMPConfigParameters.objects.all().delete()
        snmp_config_parameters_form = SNMPConfigParametersForm()

        warning_status_message = 'Removed All SNMPv3 Configurations...'

    elif 'run_snmp_config' in request.POST:
        object_ids = dict(request.POST).get('id')
        access_cf_obj_id = object_ids[0]
        snmp_cf_obj_id = object_ids[1]

        config, login_params = parse_initial_config(access_cf_obj_id)
        snmp_config_commands = parse_snmp_config(snmp_cf_obj_id)

        available_hosts = [host.network_address for host in AvailableDevices.objects.all()]
        connection = ConnectionManager(config, login_params, available_hosts)
        output = connection.connect_and_configure_multiple(snmp_config_commands)

        if output is None:
            error_status_message = 'Check Your Connection Or Access Credentials.'
        else:
            success_status_message = 'SNMPv3 Configuration Completed.'

    elif 'available_hosts' in request.POST:
        object_id = dict(request.POST).get('id')[0]
        AvailableDevices.objects.all().delete()
        config, _ = parse_initial_config(object_id)

        available_hosts = ping_all(config)

        for host in available_hosts:
            new_host = AvailableDevices(user=user, network_address=host)
            new_host.save()

        device_count = len(available_hosts)

        if device_count > 0:
            success_status_message = '{device_count} device(s) available!'.format(device_count=device_count)
        else:
            error_status_message = 'No devices available in specified network!'

    context = {
        'access_config_parameters_list': ConfigParameters.objects.filter(user=request.user),
        'snmp_config_parameters_list': SNMPConfigParameters.objects.filter(user=request.user),
        'available_hosts': AvailableDevices.objects.filter(user=request.user),
        'config_parameters_form': config_parameters_form,
        'snmp_config_parameters_form': snmp_config_parameters_form,
        'protocol': discovery_protocol,
        'device_os': device_os.keys(),
        'error_status_message': error_status_message,
        'success_status_message': success_status_message,
        'warning_status_message': warning_status_message,
    }

    return render(request, 'config_network.html', context)
