import pytest

from django.contrib.auth.models import User
from config_app.models import ConfigParameters, SNMPConfigParameters, AvailableDevices

pytestmark = pytest.mark.django_db


@pytest.mark.run(order=4)
class TestConfigParametersModel:
    def setup_method(self):
        self.user = User.objects.get(username='test_username')

        config_data = dict(
            user=self.user,
            login_username='test_user_123',
            login_password='test_password_123',
            network_ip='127.0.0.1',
            network_device_os='IOS',
            secret='test_secret_123',
            subnet_cidr='24'
        )
        self.config_parameters = ConfigParameters.objects.create(**config_data)

    def test_model(self):
        assert self.config_parameters.user == self.user
        assert self.config_parameters.login_username == 'test_user_123'
        assert self.config_parameters.login_password == 'test_password_123'
        assert self.config_parameters.network_ip == '127.0.0.1'
        assert self.config_parameters.network_device_os == 'IOS'
        assert self.config_parameters.secret == 'test_secret_123'
        assert self.config_parameters.subnet_cidr == '24'


@pytest.mark.run(order=5)
class TestAvailableDevices:
    def setup_method(self):
        self.user = User.objects.get(username='test_username')
        self.ip_address = '192.168.0.2'

        data = dict(
            user=self.user,
            network_address=self.ip_address
        )

        self.available_device = AvailableDevices.objects.create(**data)

    def test_model(self):
        assert self.available_device.user == self.user
        assert self.available_device.network_address == self.ip_address
