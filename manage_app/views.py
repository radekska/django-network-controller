from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from config_app.models import SNMPConfigParameters
from manage_app.models import DeviceModel
from manage_app.backend.get_device import DeviceManager


# Create your views here.
@login_required(redirect_field_name='')
def manage_network_view(request):
    user = User.objects.filter(username=request.user)[0]
    snmp_config_id = 1

    if 'get_devices_details' in request.POST:
        device = DeviceManager(user, snmp_config_id)
        device_details = device.get_device_details('192.168.8.129')
        DeviceModel.objects.create(user=user, device_hostname=device_details.system_name,
                                   system_description=device_details.system_description)

    return render(request, 'manage_network.html', {})
