from django.views.generic import ListView
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#
#         if user is not None:
#             login(request, user)
#             return redirect('/dashboard')
#         else:
#             error_message = 'Invalid credentials!'
#             return render(request, 'login.html', {'error_message': error_message})
#
#     elif request.user.is_authenticated:
#         return redirect('/dashboard')
#
#     return render(request, 'login.html', {})
#
#
# def logout_view(request):
#     logout(request)
#     return redirect('/login')


class LoginView(ListView):
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
    template_name = 'login.html'
    model = User

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('/login')