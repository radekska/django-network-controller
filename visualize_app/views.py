from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from visualize_app.backend.NetworkMapper import NetworkMapper


@login_required(redirect_field_name='')
def visualize_network_view(request):
    my_map = NetworkMapper()
    my_map.generate_graph_data()
    return render(request, 'visualize.html', {})
