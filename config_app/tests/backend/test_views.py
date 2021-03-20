import pytest
from django.test import Client
from django.contrib.auth.models import User


@pytest.fixture
def test_user() -> User:
    return User.objects.create_user(username='pytest_user', email='pytest_user@gmail.com',
                                    password='pytest_password')


@pytest.mark.django_db(transaction=True)
@pytest.mark.run(order=9)
class TestAccessConfigView:
    def setup_method(self):
        self.client = Client()
        self.path = "/dashboard/config_network/"

    def test_get_request(self, test_user):
        self.client.force_login(test_user)
        response = self.client.get(path=self.path)
        assert response.status_code == 200

    def test_post_add_access_config(self, test_user):
        self.client.force_login(test_user)
        test_data = dict(
            login_username="test_user",
            login_password="test_password",
            secret="secret_password",
            network_ip="1.1.1.1",
            subnet_cidr="24",
            network_device_os="Test OS",
            add_access_config="Add"
        )

        response = self.client.post(self.path, data=test_data)
        assert response.status_code == 200
        assert ' This field is required.' not in response.content.decode(
            'utf-8')

    def test_post_invalid_access_config(self, test_user):
        self.client.force_login(test_user)
        invalid_test_data = dict(
            login_username="test_user",
            login_password="test_password",
            secret="secret_password",
            network_ip="11111",
            subnet_cidr="35",
            network_device_os="Test OS",
            add_access_config="Add"
        )

        response = self.client.post(self.path, data=invalid_test_data)
        received_content = response.content.decode('utf-8')
        assert response.status_code == 200
        assert "Enter a valid IPv4 or IPv6 address." in received_content
        assert "Ensure this value is less than or equal to 32." in received_content


@pytest.mark.django_db(transaction=True)
@pytest.mark.run(order=9)
class TestSNMPConfigView:
    def setup_method(self):
        self.client = Client()
        self.path = "/dashboard/config_network/"

    def test_get_request(self, test_user):
        self.client.force_login(test_user)
        response = self.client.get(path=self.path)
        assert response.status_code == 200

    def test_post_request(self, test_user):
        self.client.force_login(test_user)
        test_data = dict(
            group_name='test_group',
            snmp_user='test_user',
            snmp_password='test_pass',
            snmp_encrypt_key='test_key',
            snmp_host='192.168.1.106',
            snmp_auth_protocol='MD5',
            snmp_privacy_protocol='AES 128',
            server_location='test_location',
            contact_details='test_contact@gmail.com',
            add_snmp_config='Add'
        )
        response = self.client.post(self.path, data=test_data)
        response_content = response.content.decode('utf-8')
        assert response.status_code == 200
        assert "SNMPv3 Configuration Added Successfully!" in response_content
        assert "This Field Is Required." not in response_content

    def test_post_invalid_snmp_config(self, test_user):
        self.client.force_login(test_user)
        invalid_test_data = dict(
            group_name='test_group',
            snmp_user='test_user',
            snmp_password='short',
            snmp_encrypt_key='test_key',
            snmp_host='111111wrong',
            snmp_auth_protocol='MD5',
            snmp_privacy_protocol='AES 128',
            server_location='test_location',
            contact_details='not_valid_email',
            add_snmp_config='Add'
        )

        response = self.client.post(self.path, data=invalid_test_data)
        received_content = response.content.decode('utf-8')
        assert response.status_code == 200
        assert "Ensure this value has at least 8 characters" in received_content
        assert "Enter a valid IPv4 or IPv6 address." in received_content
        assert "Enter a valid email address." in received_content
        assert "SNMPv3 Configuration Added Successfully!" not in response_content
