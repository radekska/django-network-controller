from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import ListView, View

from .models import ConfigParameters, SNMPConfigParameters
from .models import AvailableDevices

from .forms import ConfigParametersForm, SNMPConfigParametersForm

from .backend.static import discovery_protocol, device_os_napalm, snmp_auth_protocols, snmp_privacy_protocols
from .backend.ConfigManager import ConfigManager
from .backend.parsers import parse_initial_config, parse_snmp_config
from .backend.helpers import ping_all, get_available_devices


class ConfigNetworkView(ListView):
    """
    This class based view inherits from ListView class and handles all synchronous POST/GET requests issued from client.
    """
    template_name = 'config_network.html'
    model = User

    success_status_message = None
    warning_status_message = None
    success_status_message_list = None
    error_status_message_list = None
    error_status_message = None
    config_parameters_form = None
    snmp_config_parameters_form = None
    access_config_parameters_list = None
    snmp_config_parameters_list = None
    available_hosts = None
    protocol = None
    device_os = None
    auth_protocols = None
    privacy_protocols = None

    def _post_access_config(self, request):
        self.config_parameters_form = ConfigParametersForm(request.POST or None)
        if self.config_parameters_form.is_valid():
            access_config_model = self.config_parameters_form.save(commit=False)
            access_config_model.user = request.user
            access_config_model.save()

            self.success_status_message = 'Access Configuration Added Successfully!'

    def _post_snmp_config(self, request):
        self.snmp_config_parameters_form = SNMPConfigParametersForm(request.POST or None)
        if self.snmp_config_parameters_form.is_valid():
            snmp_config_model = self.snmp_config_parameters_form.save(commit=False)
            snmp_config_model.user = request.user
            snmp_config_model.save()

            self.success_status_message = 'SNMPv3 Configuration Added Successfully!'

    def _delete_access_config_all(self):
        AvailableDevices.objects.all().delete()
        ConfigParameters.objects.all().delete()
        self.config_parameters_form = ConfigParametersForm()

        self.warning_status_message = 'Removed All Access Configurations...'

    def _delete_snmp_config_all(self):
        SNMPConfigParameters.objects.all().delete()
        self.snmp_config_parameters_form = SNMPConfigParametersForm()

        self.warning_status_message = 'Removed All SNMPv3 Configurations...'

    def _manage_configuration_task(self, request):
        object_ids = dict(request.POST).get('id', None)
        if object_ids:
            access_cf_obj_id = object_ids[0]
            snmp_cf_obj_id = object_ids[1]

            config, login_params = parse_initial_config(access_cf_obj_id)

            available_hosts = get_available_devices()
            connection = ConfigManager(config, login_params, available_hosts)

            snmp_config_commands = parse_snmp_config(snmp_cf_obj_id)

            if 'run_snmp_config' in request.POST:
                output = connection.connect_and_configure_multiple(config_commands=snmp_config_commands)
                ConfigParameters.objects.all().update(snmp_config_id=None)

                config_model = ConfigParameters.objects.get(id=access_cf_obj_id)
                config_model.snmp_config_id = snmp_cf_obj_id
                config_model.access_config_id = access_cf_obj_id
                config_model.save()

            else:
                output = connection.connect_and_configure_multiple(config_commands=snmp_config_commands,
                                                                   type_of_change='rollback')
                ConfigParameters.objects.all().update(snmp_config_id=None)

            self.error_status_message_list = list(filter(lambda conn: conn[2] == 'error', output))
            self.success_status_message_list = list(filter(lambda conn: conn[2] == 'success', output))
            available_hosts = [host[0] for host in self.success_status_message_list]

            AvailableDevices.objects.all().delete()
            for available_host in available_hosts:
                AvailableDevices.objects.create(user=request.user, network_address=available_host)

    def _get_available_hosts(self, request):
        object_id = request.POST.get('id')[0]
        AvailableDevices.objects.all().delete()
        config, _ = parse_initial_config(object_id)

        available_hosts = ping_all(config)

        for host in available_hosts:
            new_host = AvailableDevices(user=request.user, network_address=host)
            new_host.save()

        device_count = len(available_hosts)

        if device_count > 0:
            self.success_status_message = '{device_count} device(s) available!'.format(device_count=device_count)
        else:
            self.error_status_message = 'No devices available in specified network!'

    def _fill_template_data(self, request):
        self.access_config_parameters_list = ConfigParameters.objects.filter(user=request.user)
        self.snmp_config_parameters_list = SNMPConfigParameters.objects.filter(user=request.user)
        self.available_hosts = AvailableDevices.objects.filter(user=request.user)
        self.protocol = discovery_protocol
        self.device_os = device_os_napalm.keys()
        self.auth_protocols = snmp_auth_protocols
        self.privacy_protocols = snmp_privacy_protocols

    def get(self, request, *args, **kwargs):
        self._fill_template_data(request)
        context = dict(
            access_config_parameters_list=self.access_config_parameters_list,
            snmp_config_parameters_list=self.snmp_config_parameters_list,
            available_hosts=self.available_hosts,
            protocol=self.protocol,
            device_os=self.device_os,
            auth_protocols=self.auth_protocols,
            privacy_protocols=self.privacy_protocols
        )

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        print(request.POST)
        if 'add_access_config' in request.POST:
            self._post_access_config(request)
        elif 'add_snmp_config' in request.POST:
            self._post_snmp_config(request)
        elif 'access_delete_all' in request.POST:
            self._delete_access_config_all()
        elif 'snmp_delete_all' in request.POST:
            self._delete_snmp_config_all()
        elif 'run_snmp_config' in request.POST or 'remove_snmp_config' in request.POST:
            self._manage_configuration_task(request)
        elif 'available_hosts' in request.POST:
            self._get_available_hosts(request)

        self._fill_template_data(request)
        context = dict(
            success_status_message=self.success_status_message,
            warning_status_message=self.warning_status_message,
            success_status_message_list=self.success_status_message_list,
            error_status_message_list=self.error_status_message_list,
            error_status_message=self.error_status_message,
            config_parameters_form=self.config_parameters_form,
            snmp_config_parameters_form=self.snmp_config_parameters_form,
            access_config_parameters_list=self.access_config_parameters_list,
            snmp_config_parameters_list=self.snmp_config_parameters_list,
            available_hosts=self.available_hosts,
            protocol=self.protocol,
            device_os=self.device_os,
            auth_protocols=self.auth_protocols,
            privacy_protocols=self.privacy_protocols
        )
        return render(request, self.template_name, context)
