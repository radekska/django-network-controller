from manage_app.backend.mixins.JSONResponseMixin import JSONResponseMixin
from config_app.models import ConfigParameters, SNMPConfigParameters

from django.views.generic import View
from django.http import JsonResponse, Http404
from manage_app.backend import tasks

task = None


class AjaxTrapEngineView(JSONResponseMixin, View):

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            snmp_config_id = ConfigParameters.objects.filter(snmp_config_id__isnull=False)[0].snmp_config_id

            self.snmp_config = SNMPConfigParameters.objects.get(id=snmp_config_id)
            self.traps_engine_running = self.snmp_config.traps_activated
            traps_enabled = self.snmp_config.enable_traps
            method_call = request.POST.get('button')

            if method_call == 'start' and traps_enabled and not self.traps_engine_running:
                self._post_start_trap_engine()
            elif method_call == 'stop' and traps_enabled and self.traps_engine_running:
                self._post_stop_trap_engine()

            json_data = dict(traps_engine_running=self.traps_engine_running)
            return self.render_to_response(json_data)

        else:
            raise Http404

    def _post_start_trap_engine(self):
        global task
        snmp_host = self.snmp_config.snmp_host
        privacy_protocol = self.snmp_config.snmp_privacy_protocol.replace(' ', '')

        session_parameters = dict(
            hostname=None,
            version=3,
            security_level='auth_with_privacy',
            security_username=self.snmp_config.snmp_user,
            privacy_protocol=privacy_protocol,
            privacy_password=self.snmp_config.snmp_encrypt_key,
            auth_protocol=self.snmp_config.snmp_auth_protocol,
            auth_password=self.snmp_config.snmp_password
        )

        task = tasks.run_trap_engine.delay(snmp_host, session_parameters)

        self.snmp_config.traps_activated = True
        self.snmp_config.save()

    def _post_stop_trap_engine(self):
        global task
        task.revoke(terminate=True, signal='SIGUSR1')

        self.snmp_config.traps_activated = False
        self.snmp_config.save()
