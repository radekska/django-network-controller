import json
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.views.generic import ListView


# Create your views here.
# def registration_view(request):
#     print(request.POST)
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password1')
#
#             user = authenticate(request, username=username, password=password)
#             login(request, user)
#             return redirect('/dashboard')
#     else:
#         form = UserCreationForm()
#
#     return render(request, 'register.html', {'form': form})


class RegistrationView(ListView):
    template_name = 'register.html'
    model = User

    username = None
    password = None

    def get(self, request, *args, **kwargs):
        form = UserCreationForm()
        return render(request, self.template_name, context={'form': form})

    def post(self, request, *args, **kwargs):
        print(request.POST)
        form = UserCreationForm(request.POST)

        print(form.is_valid())
        if form.is_valid():
            form.save()
            self.username = form.cleaned_data.get('username')
            self.password = form.cleaned_data.get('password1')

            is_authenticated = authenticate(request, username=self.username, password=self.password)
            if is_authenticated:
                login(request, is_authenticated)
                return redirect('/dashboard')

        else:
            error_messages = json.loads(form.errors.as_json())
            context = dict()
            if error_messages:
                context = dict(error_username_message=error_messages.get('username'),
                               error_password_message=error_messages.get('password1'),
                               error_password_confirm=error_messages.get('password2'))

            return render(request, self.template_name, context=context)
