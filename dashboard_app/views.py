from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic import ListView


class DashboardView(ListView):
    """
    This class based view inherits from ListView and handles GET request specified to dashboard app.
    """
    template_name = 'dashboard.html'
    model = User
    context = None

    def get(self, request, *args, **kwargs):
        if request.get_full_path() == '/dashboard/':
            dashboard_only = True
            self.context = dict(dashboard_only=dashboard_only)

        return render(request, template_name=self.template_name, context=self.context)
