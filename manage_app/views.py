import json
import logging

# Django
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
from django.core import serializers
from django.http import JsonResponse, Http404
from django.views.generic import ListView
from django.views.generic.detail import SingleObjectTemplateResponseMixin

# Models
from config_app.models import ConfigParameters, SNMPConfigParameters
from manage_app.models import DeviceModel, DeviceInterface, DeviceTrapModel, VarBindModel

# Backend
from visualize_app.backend.NetworkMapper import NetworkMapper
from .backend.DeviceManager import DeviceManager
from .backend.parse_model import parse_and_save_to_database, parse_trap_model
from .backend.webssh import main
from WebAppLAN_MonitorDjango.utils import get_available_devices

# Celery tasks
from .backend import tasks

ssh_session = None
task = None
paginator = None


#
# Create your views here.
@login_required(redirect_field_name='')
def manage_network_view(request):
    global ssh_session, task, paginator

    device_trap_models = None
    device_details_output = None
    device_interfaces_output = None
    error_status_message = None
    page_object = None

    user = User.objects.filter(username=request.user)[0]
    snmp_config_id = ConfigParameters.objects.filter(snmp_config_id__isnull=False)[0].snmp_config_id

    snmp_config = SNMPConfigParameters.objects.filter(id=snmp_config_id)[0]
    traps_enabled = snmp_config.enable_traps
    traps_engine_running = snmp_config.traps_activated

    page_number = request.GET.get('trap_page')

    # if 'get_devices_details' in request.POST:
    #     DeviceModel.objects.all().delete()
    #     DeviceInterface.objects.all().delete()
    #
    #     available_hosts = get_available_devices()
    #     device = DeviceManager(user, available_hosts, snmp_config_id)
    #     devices_details_output = device.get_multiple_device_details()
    #
    #     my_map = NetworkMapper()
    #     my_map.clear_graph_data()
    #
    #     try:
    #         parse_and_save_to_database(devices_details_output, user)
    #     except Exception as exception:
    #         logging.basicConfig(format='!!! %(asctime)s %(message)s')
    #         logging.warning(exception)
    #         error_status_message = 'System was not able to get all SNMP data - check connection...'

    if 'start_trap_engine' in request.POST:
        if traps_enabled and not traps_engine_running:
            snmp_host = snmp_config.snmp_host

            privacy_protocol = snmp_config.snmp_privacy_protocol.replace(' ', '')
            session_parameters = {
                'hostname': None,
                'version': 3,
                'security_level': 'auth_with_privacy',
                'security_username': snmp_config.snmp_user,
                'privacy_protocol': privacy_protocol,
                'privacy_password': snmp_config.snmp_encrypt_key,
                'auth_protocol': snmp_config.snmp_auth_protocol,
                'auth_password': snmp_config.snmp_password
            }

            task = tasks.run_trap_engine.delay(snmp_host, session_parameters)

            snmp_config.traps_activated = True
            snmp_config.save()

    elif 'stop_trap_engine' in request.POST:
        if traps_enabled and traps_engine_running:
            task.revoke(terminate=True, signal='SIGUSR1')

            snmp_config.traps_activated = False
            snmp_config.save()

    # elif 'device_id' in request.GET:
    #     device_id = request.GET.get('device_id')
    #
    #     device_details_output = DeviceModel.objects.filter(id=device_id)[0]
    #     device_interfaces_output = DeviceInterface.objects.filter(device_model_id=device_id)
    #
    #     device_trap_models = DeviceTrapModel.objects.filter(device_model=device_details_output)
    #
    #     trap_data = VarBindModel.objects.all()
    #     parse_trap_model(device_trap_models, trap_data)
    #
    #     paginator = Paginator(list(device_trap_models), 10)
    #     page_number = 1 if page_number is None else page_number
    #     page_object = paginator.page(page_number)

    # TO DO!!!
    # elif 'run_ssh_session' in request.POST:
    #     ssh_session = main.main()
    #     ssh_session.start()
    #     # TO DO - aktualnie przy pomocy asyncio z głównego procesu django "forkuje" się subproces ktory stawia
    #     # clienta ssh, niestety glowny watek caly czas sie kreci - trzeba przekminic jak zforkowac clienta ssha zeby
    #     # to ładnie zagrało a potem zastanowic sie jak wpakowac tego klienta do mannage_app - do zrobienia

    context = {
        'ssh_session': ssh_session,
        'device_detail_output': device_details_output,
        'device_interfaces_output': device_interfaces_output,
        'devices_details_output': DeviceModel.objects.all(),
        'devices_interfaces_output': DeviceInterface.objects.all(),
        'error_status_message': error_status_message,
        'traps_engine_running': traps_engine_running,
        'traps_enabled': traps_enabled,
        'device_trap_models': device_trap_models,
        'page_object': page_object
    }
    return render(request, 'manage_network.html', context)


#

class ManageNetworkView(ListView):
    template_name = 'manage_network.html'
    model = User

    task = None
    paginator = None
    page_object = None
    next_page = None
    device_trap_models = None
    device_detail_output = None
    device_interfaces_output = None
    error_status_message = None
    warning_status_message = None

    def _get_device_details(self, request):
        device_id = request.GET.get('device_id')

        self.device_detail_output = DeviceModel.objects.get(id=device_id)
        self.device_interfaces_output = DeviceInterface.objects.filter(device_model_id=device_id)
        self.device_trap_models = DeviceTrapModel.objects.filter(device_model_id=device_id)
        trap_data = VarBindModel.objects.all()

        parse_trap_model(self.device_trap_models, trap_data)

    def _get_traps_pages(self):
        global paginator
        paginator = Paginator(list(self.device_trap_models), 10)

        if paginator.count is 0:
            self.warning_status_message = 'No trap data found.'
        else:
            self.page_object = paginator.page(1)
        self.next_page = self.page_object.has_next()

    def _refresh_device_list(self, request):
        DeviceModel.objects.all().delete()
        DeviceInterface.objects.all().delete()

        self.available_hosts = get_available_devices()
        self.device_manager = DeviceManager(self.user, self.available_hosts, self.snmp_config_id)
        self.devices_details_output = self.device_manager.get_multiple_device_details()

        my_map = NetworkMapper()
        my_map.clear_graph_data()

        try:
            parse_and_save_to_database(self.devices_details_output, self.user)
        except Exception as exception:
            logging.warning(exception)
            self.error_status_message = 'System was not able to get all SNMP data - check connection...'

    def _get_config_details(self, request):
        self.user = User.objects.get(username=request.user)
        self.snmp_config_id = ConfigParameters.objects.filter(snmp_config_id__isnull=False)[0].snmp_config_id

        self.snmp_config = SNMPConfigParameters.objects.get(id=self.snmp_config_id)
        self.traps_enabled = self.snmp_config.enable_traps
        self.traps_engine_running = self.snmp_config.traps_activated

    def get(self, request, *args, **kwargs):
        self._get_config_details(request)
        print(request.GET)
        if 'device_id' in request.GET:
            self._get_device_details(request)
            self._get_traps_pages()
        if 'get_devices_details' in request.GET:
            self._refresh_device_list(request)

        context = dict(
            devices_details_output=DeviceModel.objects.all(),
            device_trap_models=self.device_trap_models,
            device_detail_output=self.device_detail_output,
            device_interfaces_output=self.device_interfaces_output,
            error_status_message=self.error_status_message,
            warning_status_message=self.warning_status_message,
            traps_engine_running=self.traps_engine_running,
            traps_enabled=self.traps_enabled,
            page_object=self.page_object,
            next_page=self.next_page
        )

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        self._get_config_details(request)
        if 'start_trap_engine' in request.POST and self.traps_enabled and not self.traps_engine_running:
            self._post_start_trap_engine()
        elif 'stop_trap_engine' in request.POST and self.traps_enabled and self.traps_engine_running:
            self._post_stop_trap_engine()

    def _post_start_trap_engine(self):
        global task
        snmp_host = self.snmp_config.snmp_host

        privacy_protocol = self.snmp_config.snmp_privacy_protocol.replace(' ', '')
        session_parameters = {
            'hostname': None,
            'version': 3,
            'security_level': 'auth_with_privacy',
            'security_username': self.snmp_config.snmp_user,
            'privacy_protocol': privacy_protocol,
            'privacy_password': self.snmp_config.snmp_encrypt_key,
            'auth_protocol': self.snmp_config.snmp_auth_protocol,
            'auth_password': self.snmp_config.snmp_password
        }

        task = tasks.run_trap_engine.delay(snmp_host, session_parameters)

        self.snmp_config.traps_activated = True
        self.snmp_config.save()

    def _post_stop_trap_engine(self):
        global task
        task.revoke(terminate=True, signal='SIGUSR1')

        self.snmp_config.traps_activated = False
        self.snmp_config.save()


@login_required(redirect_field_name='')
def ajax_trap_view(request):
    if request.is_ajax():
        global paginator
        page_number = request.GET.get('page_number')
        page_object = paginator.page(page_number)

        data = serializers.serialize('json', page_object.object_list)
        trap_json_data = json.loads(data)

        json_data = {
            'trap_json_data': trap_json_data,
            'page_has_next': page_object.has_next(),
            'page_has_previous': page_object.has_previous(),
            'current_page': page_number,
            'last_page': paginator.num_pages
        }
        return JsonResponse(json_data, safe=False)
    else:
        raise Http404


@login_required(redirect_field_name='')
def ajax_trap_engine(request):
    if request.is_ajax():
        print(request.POST)
    # to do.