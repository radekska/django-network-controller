from django.views.generic import ListView
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


class LoginView(ListView):
    """
    This class based view inherits from ListView and handles POST and GET requests specified to login_app
    """
    template_name = 'login.html'
    model = User

    username = None
    password = None

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/dashboard')

        return render(request, self.template_name, context={})

    def post(self, request, *args, **kwargs):
        self.username = request.POST.get('username', None)
        self.password = request.POST.get('password', None)

        if self.username is not None and self.password is not None:
            user_authenticated = authenticate(request, username=self.username, password=self.password)
            if user_authenticated:
                login(request, user_authenticated)
                return redirect('/dashboard')
            else:
                error_status_message = 'Invalid credentials!'
                return render(request, self.template_name, context=dict(error_status_message=error_status_message))


class LogoutView(ListView):
    """
    This class based view inherits from ListView and handles GET request specified to logout url
    """

    template_name = 'login.html'
    model = User

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('/login')