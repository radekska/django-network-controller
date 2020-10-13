from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from config_app.models import SNMPConfigParameters, AvailableDevices
from manage_app.models import DeviceModel
from manage_app.backend.get_device import DeviceManager
from WebAppLAN_MonitorDjango.utils import get_available_devices


# Create your views here.
@login_required(redirect_field_name='')
def manage_network_view(request):
    user = User.objects.filter(username=request.user)[0]
    snmp_config_id = 1
    devices_details_output = None

    if 'get_devices_details' in request.POST:
        available_hosts = get_available_devices()
        device = DeviceManager(user, available_hosts, snmp_config_id)
        devices_details_output = device.get_multiple_device_details()

    for dev in devices_details_output:
        print(dev.system.system_name)
        for interface in dev.interfaces:
            print(interface.interface_name, interface.interface_admin_status)
    context = {
        'devices_details_output': devices_details_output
    }

    # TO DO - rozbudować dalej te klasy dodac im wiecej parametrow,
    # dlubac w oidach i mibach no i wiadomo później tabelka na manage app i lecimy daleeej :D

    return render(request, 'manage_network.html', context)
