from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import ConfigParameters
from .forms import ConfigParametersForm

from .backend.static import discovery_protocol, device_os
from .backend.initial_config import Config
from .backend.parse_model import parse_config


# Create your views here.
@login_required(redirect_field_name='')
def config_network_view(request):
    form = ConfigParametersForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()

    if 'delete_all' in request.POST:
        ConfigParameters.objects.all().delete()
        form = ConfigParametersForm()

    elif 'run_config' in request.POST:
        form = ConfigParametersForm()
        object_id = request.POST.get('id')
        print('here')
        config, login_params = parse_config(object_id)
        initial_config = Config(config, login_params)
        print('there')
        cf_output = initial_config.conf_disc_proto()
        print(cf_output)
        for output in cf_output:
            print(output)

    context = {
        'parameters_list': ConfigParameters.objects.filter(user=request.user),
        'form': form,
        'protocol': discovery_protocol,
        'device_os': device_os.keys(),
    }

    return render(request, 'config_network.html', context)
