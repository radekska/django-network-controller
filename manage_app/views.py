import json
import logging

# Django
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core import serializers
from django.http import JsonResponse, Http404
from django.views.generic import ListView, View

# Models
from config_app.models import ConfigParameters, SNMPConfigParameters
from manage_app.models import DeviceModel, DeviceInterface, DeviceTrapModel, VarBindModel

# Backend
from visualize_app.backend.NetworkMapper import NetworkMapper
from .backend.DeviceManager import DeviceManager
from .backend.parse_model import parse_and_save_to_database, parse_trap_model
from config_app.backend.helpers import get_available_devices
from main_app.backend.helpers import check_if_properly_configured

# Mixins
from main_app.mixins.JSONResponseMixin import JSONResponseMixin

ssh_session = None
task = None
paginator = None


class ManageNetworkView(ListView):
    """
    This class based view inherits from ListView and handles all synchronous GET requests issued to manage section.
    """
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

    traps_engine_running = None
    traps_enabled = None

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

        if paginator.count == 0:
            self.warning_status_message = 'No trap data found.'
        else:
            self.page_object = paginator.page(1)

        try:
            self.next_page = self.page_object.has_next()
        except Exception as exception:
            logging.warning(exception)

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
        self.snmp_config_id = ConfigParameters.objects.get(snmp_config_id__isnull=False).snmp_config_id

        self.snmp_config = SNMPConfigParameters.objects.get(id=self.snmp_config_id)
        self.traps_enabled = self.snmp_config.enable_traps
        self.traps_engine_running = self.snmp_config.traps_activated

    def get(self, request, *args, **kwargs):
        properly_configured = check_if_properly_configured()

        if not all(properly_configured.values()):
            context = properly_configured
        else:
            self._get_config_details(request)

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
                next_page=self.next_page,
                initial_configurations_applied=True,
                initial_configurations=True,
            )

        return render(request, self.template_name, context)


class AjaxTrapView(JSONResponseMixin, View):
    """
    This class based view handles all AJAX GET requests for Traps and Events table pagination.
    """

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            global paginator
            page_number = request.GET.get('page_number', None)

            if page_number:
                page_object = paginator.page(page_number)

                data = serializers.serialize('json', page_object.object_list)
                trap_json_data = json.loads(data)

                json_data = dict(
                    trap_json_data=trap_json_data,
                    current_page=page_number,
                    last_page=paginator.num_pages
                )
                return self.render_to_response(json_data)

        else:
            raise Http404
