from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(redirect_field_name='')
def dashboard_view(request):
    context = None
    if request.user.is_authenticated:
        if request.get_full_path() == '/dashboard/':
            dashboard_only = True
            context = dict(dashboard_only=dashboard_only)
        return render(request, 'dashboard.html', context=context)

    return redirect('login')
