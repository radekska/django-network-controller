from django.shortcuts import render


# Create your views here.
def manage_network_view(request):
    return render(request, 'manage_network.html', {})
