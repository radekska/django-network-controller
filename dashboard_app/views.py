from django.shortcuts import render, redirect


# Create your views here.
def dashboard_view(request):
    if request.user.is_authenticated:
        return render(request, 'dashboard.html')

    return redirect('login')