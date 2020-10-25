from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from manage_app.models import DeviceModel, DeviceInterface
from visualize_app.backend.NetworkMapper import NetworkMapper


@login_required(redirect_field_name='')
def visualize_network_view(request):
    device_model = None
    neighbor_devices = None
    request_post_dict = dict(request.POST)

    my_map = NetworkMapper()
    my_map.generate_graph_data()

    if 'get_lldp_details' in request.POST:
        device_id = request_post_dict.get('get_lldp_details')[0]
        device_model = DeviceModel.objects.filter(id=device_id)[0]

        device_interfaces = DeviceInterface.objects.filter(device_model=device_model)
        device_interfaces = list(
            filter(lambda interface: interface.lldp_neighbor_hostname is not None, device_interfaces))

        neighbor_system_names = [neighbor.lldp_neighbor_hostname for neighbor in device_interfaces]

        neighbor_devices = list()

        for system_name in neighbor_system_names:
            neighbor_device = DeviceModel.objects.filter(full_system_name=system_name)[0]
            neighbor_devices.append(neighbor_device)

        neighbor_devices = zip(device_interfaces, neighbor_devices)

    context = {
        'device_model': device_model,
        'lldp_neighbor_details': neighbor_devices,
    }

    return render(request, 'visualize.html', context)
