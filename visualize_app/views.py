from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.models import User

from visualize_app.backend import NetworkMapper
from main_app.backend.helpers import check_if_properly_configured


class VisualizeNetworkView(ListView):
    """
    This class is responsible for handling all synchronous GET requests. In other words, for final rendering
    network graph.
    """
    template_name = 'visualize.html'
    model = User

    device_model = None
    lldp_neighbor_details = None

    def get(self, request, *args, **kwargs):
        properly_configured = check_if_properly_configured()

        if not all(properly_configured.values()):
            context = properly_configured
        else:
            my_map = NetworkMapper()
            my_map.generate_graph_data()

            context = dict(
                device_model=self.device_model,
                initial_configurations_applied=True,
                initial_configurations=True,
            )

        return render(request, self.template_name, context)
