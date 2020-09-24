from django.shortcuts import render, redirect
from .models import ConfigParameters
from .forms import ConfigParametersForm


# Create your views here.
def config_create_view(request):
    if request.method == 'POST':
        form = ConfigParametersForm(request.POST or None)

        if form.is_valid():
            form.save()
            return redirect('/configview/')
    else:
        form = ConfigParametersForm()

    return render(request, 'config_app/config_create.html', {'form': form})


def config_detail_view(request):
    config_obj = ConfigParameters.objects.all()

    context = {
        'config_obj': config_obj[0]
    }

    return render(request, 'config_app/config_detail.html', context)
