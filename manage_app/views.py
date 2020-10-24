from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from config_app.models import SNMPConfigParameters, AvailableDevices
from manage_app.models import DeviceModel, DeviceInterface
from .backend.DeviceManager import DeviceManager
from .backend.parse_model import parse_and_save_to_database
from .backend.webssh import main
from WebAppLAN_MonitorDjango.utils import get_available_devices

ssh_session = None


# Create your views here.
@login_required(redirect_field_name='')
def manage_network_view(request):
    global ssh_session
    device_details_output = None
    device_interfaces_output = None

    user = User.objects.filter(username=request.user)[0]
    snmp_config_id = 2

    request_post_dict = dict(request.POST)
    print(request.POST)

    if 'get_devices_details' in request.POST:
        DeviceModel.objects.all().delete()
        DeviceInterface.objects.all().delete()

        available_hosts = get_available_devices()
        device = DeviceManager(user, available_hosts, snmp_config_id)
        devices_details_output = device.get_multiple_device_details()

        parse_and_save_to_database(devices_details_output, user)

    elif 'get_device_details' in request.POST:
        device_id = request_post_dict.get('get_device_details')[0]
        device_details_output = DeviceModel.objects.filter(id=device_id)[0]
        device_interfaces_output = DeviceInterface.objects.filter(device_model_id=device_id)

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
        'devices_interfaces_output': DeviceInterface.objects.all()
    }

    return render(request, 'manage_network.html', context)
