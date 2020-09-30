from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(redirect_field_name='')
def manage_network_view(request):
    return render(request, 'manage_network.html', {})
