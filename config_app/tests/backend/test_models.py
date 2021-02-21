import pytest
from django.contrib.auth.models import User
from config_app.models import ConfigParameters, SNMPConfigParameters, AvailableDevices


@pytest.fixture
def test_user() -> User:
    return User.objects.create_user(username='pytest_user', email='pytest_user@gmail.com',
                                    password='pytest_password')


@pytest.fixture
def config_parameters(test_user) -> ConfigParameters:
    config_data = dict(
        user=test_user,
        login_username='test_user_123',
        login_password='test_password_123',
        network_ip='127.0.0.1',
        network_device_os='IOS',
        secret='test_secret_123',
        subnet_cidr='24'
    )
    return ConfigParameters.objects.create(**config_data)


@pytest.fixture
def available_devices(test_user) -> AvailableDevices:
    test_data = dict(
        user=test_user,
        network_address="192.168.0.2"
    )
    return AvailableDevices.objects.create(**test_data)


@pytest.fixture
def snmp_config_parameters(test_user):
    data = dict(
        user=test_user,
        group_name='TEST_GROUP',
        snmp_user='TEST_SNMP_USER',
        snmp_password='TEST_SNMP_PASSWORD',
        snmp_auth_protocol='TEST_AUTH_PROTOCOL',
        snmp_privacy_protocol='TEST_PRIVACY_PROTOCOL',
        snmp_encrypt_key='TEST_ENCRYPT_KEY',
        snmp_host='127.0.0.1',
        server_location='TEST_LOCATION',
        contact_details='TEST_CONTACT_DETAILS',
        enable_traps=True)

    return SNMPConfigParameters.objects.create(**data)


@pytest.mark.django_db(transaction=True)
def test_transaction_true_db_fixture(test_user, config_parameters, available_devices, snmp_config_parameters):
    assert isinstance(test_user, User)
    assert isinstance(config_parameters, ConfigParameters)
    assert isinstance(available_devices, AvailableDevices)
    assert isinstance(snmp_config_parameters, SNMPConfigParameters)


@pytest.mark.django_db(transaction=True)
@pytest.mark.run(order=4)
class TestConfigParametersModel:
    def test_model(self, config_parameters, test_user):
        assert config_parameters.user == test_user
        assert config_parameters.login_username == 'test_user_123'
        assert config_parameters.login_password == 'test_password_123'
        assert config_parameters.network_ip == '127.0.0.1'
        assert config_parameters.network_device_os == 'IOS'
        assert config_parameters.secret == 'test_secret_123'
        assert config_parameters.subnet_cidr == '24'


@pytest.mark.django_db(transaction=True)
@pytest.mark.run(order=5)
class TestAvailableDevicesModel:
    def test_model(self, test_user, available_devices):
        assert available_devices.user == test_user
        assert available_devices.network_address == "192.168.0.2"


@pytest.mark.django_db(transaction=True)
@pytest.mark.run(order=6)
class TestSNMPConfigParametersModel:
    def test_model(self, test_user, snmp_config_parameters):
        assert snmp_config_parameters.user == test_user
        assert snmp_config_parameters.group_name == 'TEST_GROUP'
        assert snmp_config_parameters.snmp_user == 'TEST_SNMP_USER'
        assert snmp_config_parameters.snmp_password == 'TEST_SNMP_PASSWORD'
        assert snmp_config_parameters.snmp_auth_protocol == 'TEST_AUTH_PROTOCOL'
        assert snmp_config_parameters.snmp_privacy_protocol == 'TEST_PRIVACY_PROTOCOL'
        assert snmp_config_parameters.snmp_encrypt_key == 'TEST_ENCRYPT_KEY'
        assert snmp_config_parameters.snmp_host == '127.0.0.1'
        assert snmp_config_parameters.server_location == 'TEST_LOCATION'
        assert snmp_config_parameters.contact_details == 'TEST_CONTACT_DETAILS'
        assert snmp_config_parameters.enable_traps is True
