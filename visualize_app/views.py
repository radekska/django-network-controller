from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(redirect_field_name='')
def visualize_network_view(request):
    return render(request, 'visualize.html', {})
