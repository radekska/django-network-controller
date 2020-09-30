from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(redirect_field_name='')
def dashboard_view(request):
    if request.user.is_authenticated:
        return render(request, 'dashboard.html')

    return redirect('login')