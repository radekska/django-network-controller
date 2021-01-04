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
class TestAvailableDevicesModel:
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


@pytest.mark.run(order=6)
class TestSNMPConfigParametersModel:
    def setup_method(self):
        self.user = User.objects.get(username='test_username')
        self.group_name = 'TEST_GROUP'
        self.snmp_user = 'TEST_SNMP_USER'
        self.snmp_password = 'TEST_SNMP_PASSWORD'
        self.snmp_auth_protocol = 'TEST_AUTH_PROTOCOL'
        self.snmp_privacy_protocol = 'TEST_PRIVACY_PROTOCOL'
        self.snmp_encrypt_key = 'TEST_ENCRYPT_KEY'
        self.snmp_host = '127.0.0.1'
        self.server_location = 'TEST_LOCATION'
        self.contact_details = 'TEST_CONTACT_DETAILS'
        self.enable_traps = True

        data = dict(
            user=self.user,
            group_name=self.group_name,
            snmp_user=self.snmp_user,
            snmp_password=self.snmp_password,
            snmp_auth_protocol=self.snmp_auth_protocol,
            snmp_privacy_protocol=self.snmp_privacy_protocol,
            snmp_encrypt_key=self.snmp_encrypt_key,
            snmp_host=self.snmp_host,
            server_location=self.server_location,
            contact_details=self.contact_details,
            enable_traps=self.enable_traps)

        self.snmp_config_parameters = SNMPConfigParameters.objects.create(**data)

    def test_model(self):
        assert self.snmp_config_parameters.user == self.user
        assert self.snmp_config_parameters.group_name == self.group_name
        assert self.snmp_config_parameters.snmp_user == self.snmp_user
        assert self.snmp_config_parameters.snmp_password == self.snmp_password
        assert self.snmp_config_parameters.snmp_auth_protocol == self.snmp_auth_protocol
        assert self.snmp_config_parameters.snmp_privacy_protocol == self.snmp_privacy_protocol
        assert self.snmp_config_parameters.snmp_encrypt_key == self.snmp_encrypt_key
        assert self.snmp_config_parameters.snmp_host == self.snmp_host
        assert self.snmp_config_parameters.server_location == self.server_location
        assert self.snmp_config_parameters.contact_details == self.contact_details
        assert self.snmp_config_parameters.enable_traps == self.enable_traps
