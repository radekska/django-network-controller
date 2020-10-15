from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from config_app.models import SNMPConfigParameters, AvailableDevices
from manage_app.models import DeviceModel, DeviceInterface
from .backend.get_device import DeviceManager
from .backend.parse_model import parse_and_save_to_database
from WebAppLAN_MonitorDjango.utils import get_available_devices


# Create your views here.
@login_required(redirect_field_name='')
def manage_network_view(request):
    user = User.objects.filter(username=request.user)[0]
    snmp_config_id = 1

    if 'get_devices_details' in request.POST:
        DeviceModel.objects.all().delete()
        DeviceInterface.objects.all().delete()

        available_hosts = get_available_devices()
        device = DeviceManager(user, available_hosts, snmp_config_id)
        devices_details_output = device.get_multiple_device_details()

        parse_and_save_to_database(devices_details_output, user)

    context = {
        'devices_details_output': DeviceModel.objects.all(),
        'devices_interfaces_output': DeviceInterface.objects.all()
    }

    # TO DO - rozbudować dalej te klasy dodac im wiecej parametrow,
    # dlubac w oidach i mibach no i wiadomo później tabelka na manage app i lecimy daleeej :D

    return render(request, 'manage_network.html', context)
