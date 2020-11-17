import manage_app.views , manage_app.backend.mixins
import config_app.views
import visualize_app.views

from . import views
from django.urls import path
from django.conf.urls import url
from django.contrib.auth.decorators import login_required



urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('config_network/', config_app.views.config_network_view, name='config_network'),
    path('manage_network/', login_required(manage_app.views.ManageNetworkView.as_view()), name='manage_network'),
    path('manage_network/ajax/pages/', manage_app.views.ajax_trap_view, name='ajax_trap_view'),
    path('manage_network/ajax/engine/', login_required(manage_app.backend.mixins.AjaxTrapEngineView.as_view()), name='ajax_trap_engine'),
    path('manage_network/ajax/ssh/', login_required(manage_app.backend.mixins.AjaxSSHSessionView.as_view()), name='ajax_ssh_session'),
    path('visualize_network/', login_required(visualize_app.views.VisualizeNetworkView.as_view()), name='visualize_network'),

]
