import config_app.views
import manage_app.views
import visualize_app.views

from . import views
from django.urls import path


urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('config_network/', config_app.views.config_network_view, name='config_network'),
    path('manage_network/', manage_app.views.manage_network_view, name='manage_network'),
    path('visualize_network/', visualize_app.views.visualize_network_view, name='visualize_network'),

]
