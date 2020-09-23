from django import forms
from .models import ConfigParameters


class ConfigParametersForm(forms.ModelForm):
    class Meta:
        model = ConfigParameters
        fields = [
            'username',
            'password',
            'secret',
            'network_ip',
            'subnet',
            'network_device_os',
            'discovery_protocol'
        ]
        widgets = {
            'password': forms.PasswordInput(),
            'secret': forms.PasswordInput(),
        }






