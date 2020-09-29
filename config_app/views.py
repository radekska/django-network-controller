from django.shortcuts import render
from .models import ConfigParameters
from .forms import ConfigParametersForm
from .static import discovery_protocols, device_os


# Create your views here.
def config_network_view(request):
    form = ConfigParametersForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()

    context = {
        'parameters_list': ConfigParameters.objects.filter(user=request.user),
        'form': form,
        'protocols': discovery_protocols,
        'device_os': device_os
    }

    print(request.POST)
    return render(request, 'config_network.html', context)


def config_detail_view(request):
    config_obj = ConfigParameters.objects.all()

    context = {
        'config_obj': config_obj[0]
    }

    return render(request, 'config_app/config_detail.html', context)
