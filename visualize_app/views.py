from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from manage_app.models import DeviceModel, DeviceInterface
from visualize_app.backend.NetworkMapper import NetworkMapper


class VisualizeNetworkView(ListView):
    template_name = 'visualize.html'
    model = User

    device_model = None
    lldp_neighbor_details = None

    def get(self, request, *args, **kwargs):
        my_map = NetworkMapper()
        my_map.generate_graph_data()

        context = dict(
            device_model=self.device_model,
        )

        return render(request, self.template_name, context)
