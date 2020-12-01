from django.views.generic import View
from django.http import Http404

from main_app.mixins.JSONResponseMixin import JSONResponseMixin
from manage_app.models import DeviceModel


class AjaxSSHSessionView(JSONResponseMixin, View):
    """
    This class based view inherits from JSONResponseMixin and View class
    and creates proper method to handle asynchronous POST request for running SSH web terminal session.

    If request is AJAX it returns json object otherwise raises Http404
    """

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            device_id = request.POST.get('device_id', None)
            method = request.POST.get('button')
            if device_id:
                if method == 'start':
                    device_model = DeviceModel.objects.get(id=device_id)
                    device_model.ssh_session = True
                    device_model.save()

                    json_data = dict(device_id=device_id, status='Session started')
                    return self.render_to_response(json_data)
                elif method == 'stop':
                    device_model = DeviceModel.objects.get(id=device_id)
                    device_model.ssh_session = False
                    device_model.save()

                    json_data = dict(device_id=device_id, status='Session stopped')
                    return self.render_to_response(json_data)
        else:
            raise Http404
