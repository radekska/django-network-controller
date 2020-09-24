from django import forms
from .models import ConfigParameters


class ConfigParametersForm(forms.ModelForm):
    class Meta:
        model = ConfigParameters
        fields = [
            'login_username',
            'login_password',
            'secret',
            'network_ip',
            'subnet_CIDR',
            'network_device_os',
            'discovery_protocol'
        ]
        widgets = {
            'login_password': forms.PasswordInput(),
            'secret': forms.PasswordInput(),
        }






