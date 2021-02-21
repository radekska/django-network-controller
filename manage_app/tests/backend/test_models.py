import pytest

from django.contrib.auth.models import User
from manage_app.models import DeviceModel, DeviceInterface, DeviceTrapModel, VarBindModel


@pytest.fixture
def test_user() -> User:
    return User.objects.create_user(username='pytest_user', email='pytest_user@gmail.com',
                                    password='pytest_password')


@pytest.fixture
def test_device(test_user):
    test_data = dict(
        user=test_user,
        system_description="Cisco IOS",
        system_version="Version 1.0",
        system_image="IOSv",
        system_type="Test type",
        system_contact="rskalban",
        full_system_name="Test system name",
        system_location="Test location",
        system_up_time="10000",
        if_number="5",
        device_type="Router",
        hostname="TestRouter",
        ssh_session=False
    )

    return DeviceModel.objects.create(**test_data)


@pytest.fixture
def test_device_interface(test_user, test_device):
    test_data = dict(
        user=test_user,
        device_model=test_device,
        interface_name="TEST INTERFACE",
        interface_description="TEST DESCRIPTION",
        interface_mtu="1500",
        interface_speed="10000000",
        interface_physical_addr="AA:BB:CC:DD:EE:FF",
        interface_admin_status="Down",
        interface_operational_status="Down",
        interface_ip="1.1.1.1"
    )
    return DeviceInterface.objects.create(**test_data)


@pytest.fixture
def device_trap_model(test_device):
    test_data = dict(
        device_model=test_device,
        trap_date="2021/02/21",
        trap_domain="TEST DOMAIN",
        trap_address="1.1.1.1",
        trap_port="165",
        trap_string_data="TEST TRAP DATA"
    )
    return DeviceTrapModel.objects.create(**test_data)


@pytest.fixture
def trap_bind_model(device_trap_model):
    test_data = dict(
        trap_model=device_trap_model,
        trap_oid="TEST OID",
        trap_data="TEST TRAP DATA",
    )

    return VarBindModel.objects.create(**test_data)


@pytest.mark.run(order=10)
@pytest.mark.django_db(transaction=True)
def test_transaction_true_db_fixture(test_user, test_device, test_device_interface, device_trap_model):
    assert isinstance(test_user, User)
    assert isinstance(test_device, DeviceModel)
    assert isinstance(test_device_interface, DeviceInterface)
    assert isinstance(device_trap_model, DeviceTrapModel)


@pytest.mark.django_db(transaction=True)
@pytest.mark.run(order=11)
class TestDeviceModel:
    def test_device_model(self, test_user, test_device):
        assert test_device.user == test_user
        assert test_device.system_description == "Cisco IOS"
        assert test_device.system_version == "Version 1.0"
        assert test_device.system_type == "Test type"
        assert test_device.system_image == "IOSv"
        assert test_device.system_contact == "rskalban"
        assert test_device.full_system_name == "Test system name"
        assert test_device.system_location == "Test location"
        assert test_device.system_up_time == "10000"
        assert test_device.if_number == "5"
        assert test_device.device_type == "Router"
        assert test_device.hostname == "TestRouter"
        assert test_device.ssh_session is False


@pytest.mark.django_db(transaction=True)
@pytest.mark.run(order=12)
class TestDeviceInterface:
    def test_device_interface(self, test_user, test_device, test_device_interface):
        assert test_device_interface.user == test_user
        assert test_device_interface.device_model == test_device
        assert test_device_interface.interface_name == "TEST INTERFACE"
        assert test_device_interface.interface_description == "TEST DESCRIPTION"
        assert test_device_interface.interface_mtu == "1500"
        assert test_device_interface.interface_speed == "10000000"
        assert test_device_interface.interface_physical_addr == "AA:BB:CC:DD:EE:FF"
        assert test_device_interface.interface_admin_status == "Down"
        assert test_device_interface.interface_operational_status == "Down"
        assert test_device_interface.interface_ip == "1.1.1.1"


@pytest.mark.django_db(transaction=True)
@pytest.mark.run(order=13)
class TestDeviceTrapModel:
    def test_device_trap_model(self, test_device, device_trap_model):
        assert device_trap_model.device_model == test_device
        assert device_trap_model.trap_date == "2021/02/21"
        assert device_trap_model.trap_domain == "TEST DOMAIN"
        assert device_trap_model.trap_address == "1.1.1.1"
        assert device_trap_model.trap_port == "165"
        assert device_trap_model.trap_string_data == "TEST TRAP DATA"


@pytest.mark.django_db(transaction=True)
@pytest.mark.run(order=14)
class TestVarBindModel:
    def test_var_bind_model(self, device_trap_model, trap_bind_model):
        assert trap_bind_model.trap_model == device_trap_model
        assert trap_bind_model.trap_oid == "TEST OID"
        assert trap_bind_model.trap_data == "TEST TRAP DATA"
