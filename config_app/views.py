from django.shortcuts import render, redirect
from .models import ConfigParameters
from .forms import ConfigParametersForm


# Create your views here.
def config_network_view(request):
    context = dict()

    if request.method == 'POST':
        form = ConfigParametersForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()

    else:
        context = {
            'parameters_list': ConfigParameters.objects.filter(user=request.user),
            'form': ConfigParametersForm()
        }

    return render(request, 'config_network.html', context)


def config_detail_view(request):
    config_obj = ConfigParameters.objects.all()

    context = {
        'config_obj': config_obj[0]
    }

    return render(request, 'config_app/config_detail.html', context)
