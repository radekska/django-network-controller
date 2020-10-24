from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from manage_app.models import DeviceModel, DeviceInterface
from visualize_app.backend.NetworkMapper import NetworkMapper


@login_required(redirect_field_name='')
def visualize_network_view(request):
    device_model = None
    device_interfaces = None
    request_post_dict = dict(request.POST)

    my_map = NetworkMapper()
    my_map.generate_graph_data()

    if 'get_lldp_details' in request.POST:
        device_id = request_post_dict.get('get_lldp_details')[0]
        device_model = DeviceModel.objects.filter(id=device_id)[0]
        device_interfaces = DeviceInterface.objects.filter(device_model=device_model)
        device_interfaces = list(
            filter(lambda interface: interface.lldp_neighbor_hostname is not None, device_interfaces))

    context = {
        'device_model': device_model,
        'lldp_neighbor_details': device_interfaces
    }

    print(device_interfaces, type(device_interfaces))
    return render(request, 'visualize.html', context)
