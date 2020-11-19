"""WebAppLAN_MonitorDjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

import dashboard_app.urls

from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from login_app.views import LoginView, LogoutView
from registration_app.views import RegistrationView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', LoginView.as_view(), name='login'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', login_required(LogoutView.as_view()), name='logout'),
    path('registration/', RegistrationView.as_view(), name='registration'),

    path('dashboard/', include('dashboard_app.urls')),


    # Built in path to login view
    # path('', include('django.contrib.auth.urls')),

]

urlpatterns += staticfiles_urlpatterns()
