from main_app.mixins.JSONResponseMixin import JSONResponseMixin
from manage_app.models import DeviceModel, DeviceInterface

from django.views.generic import View
from django.http import Http404
from django.forms.models import model_to_dict


class AjaxDeviceNeighborsView(JSONResponseMixin, View):
    """
    This class based view is responsible for handling AJAX GET requests. It takes from GET request a device_id data
    and uses it to render neighbors data based on specified (from user perspective - topology clicked) device.
    """
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            device_id = request.GET.get('device_id', None)
            if device_id:
                device_model = DeviceModel.objects.get(id=device_id)

                device_interfaces = DeviceInterface.objects.filter(device_model=device_model)
                device_interfaces = list(
                    filter(lambda interface: interface.lldp_neighbor_hostname is not None, device_interfaces))

                neighbor_system_names = [neighbor.lldp_neighbor_hostname for neighbor in device_interfaces]
                neighbor_devices = list()

                for system_name in neighbor_system_names:
                    neighbor_device = DeviceModel.objects.get(full_system_name=system_name)
                    neighbor_devices.append(neighbor_device)

                lldp_neighbor_details = zip(device_interfaces, neighbor_devices)
                serialized = list()

                for neighbor_pair in lldp_neighbor_details:
                    serialized_interface_model = model_to_dict(neighbor_pair[0])
                    serialized_device_model = model_to_dict(neighbor_pair[1])

                    serialized.append({**serialized_interface_model, **serialized_device_model})

                return self.render_to_response(serialized)

        else:
            return Http404
