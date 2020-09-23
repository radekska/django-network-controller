from django.shortcuts import render
from .models import ConfigParameters
from .forms import ConfigParametersForm


# Create your views here.
def config_create_view(request):
    form = ConfigParametersForm(request.POST or None)
    if form.is_valid():
        form.save()

    context = {
        'form': form
    }
    return render(request, 'config_app/config_create.html', context)


def config_detail_view(request):
    config_obj = ConfigParameters.objects.get(id=1)

    context = {
        'config_obj': config_obj
    }

    return render(request, 'config_app/config_detail.html', context)
