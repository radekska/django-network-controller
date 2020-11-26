from manage_app.backend.mixins.JSONResponseMixin import JSONResponseMixin
from manage_app.models import DeviceModel

from django.views.generic import View
from django.http import JsonResponse, Http404


class AjaxSSHSessionView(JSONResponseMixin, View):
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            print(request.POST)
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
