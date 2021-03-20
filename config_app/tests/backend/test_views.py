import pytest
from config_app.tests.backend import static
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
            login_username=static.CORRECT_LOGIN_USERNAME,
            login_password=static.CORRECT_LOGIN_PASSWORD,
            secret=static.CORRECT_SECRET,
            network_ip=static.CORRECT_NETWORK_IP,
            subnet_cidr=static.CORRECT_CIDR,
            network_device_os=static.CORRECT_NETWORK_DEVICE_OS,
            add_access_config=static.ADD_ACCESS_CONFIG
        )

        response = self.client.post(self.path, data=test_data)
        received_content = response.content.decode('utf-8')
        assert response.status_code == 200
        assert static.FIELD_REQUIRED not in received_content
        assert static.ADD_ACCESS_CONFIG_SUC in received_content

    def test_post_invalid_access_config(self, test_user):
        self.client.force_login(test_user)
        invalid_test_data = dict(
            login_username=static.CORRECT_LOGIN_USERNAME,
            login_password=static.CORRECT_LOGIN_PASSWORD,
            secret=static.CORRECT_SECRET,
            network_ip=static.INCORRECT_NETWORK_IP,
            subnet_cidr=static.INCORRECT_CIDR,
            network_device_os=static.CORRECT_NETWORK_DEVICE_OS,
            add_access_config=static.ADD_ACCESS_CONFIG
        )

        response = self.client.post(self.path, data=invalid_test_data)
        received_content = response.content.decode('utf-8')
        assert response.status_code == 200
        assert static.ENTER_VALID_IP in received_content
        assert static.ENTER_VALID_CIDR in received_content

    def test_access_configuration_list_details(self, test_user):
        self.client.force_login(test_user)
        self.test_post_add_access_config(test_user)
        response = self.client.get(self.path)
        received_content = response.content.decode('utf-8')

        assert static.CORRECT_LOGIN_USERNAME in received_content
        assert static.CORRECT_LOGIN_PASSWORD in received_content
        assert static.CORRECT_SECRET in received_content
        assert static.CORRECT_NETWORK_IP in received_content
        assert static.CORRECT_CIDR in received_content
        assert static.CORRECT_NETWORK_DEVICE_OS in received_content


# noinspection DuplicatedCode
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
            group_name=static.VALID_GROUP_NAME,
            snmp_user=static.VALID_SNMP_USER,
            snmp_password=static.VALID_SNMP_PASSWORD,
            snmp_encrypt_key=static.VALID_SNMP_ENCRYPT_KEY,
            snmp_host=static.VALID_SNMP_HOST,
            snmp_auth_protocol=static.VALID_SNMP_AUTH_PROTOCOL,
            snmp_privacy_protocol=static.VALID_SNMP_PRIVACY_PROTOCOL,
            server_location=static.VALID_SERVER_LOCATION,
            contact_details=static.VALID_CONTACT_DETAILS,
            add_snmp_config=static.VALID_ADD_SNMP_CONFIG
        )
        response = self.client.post(self.path, data=test_data)
        response_content = response.content.decode('utf-8')
        assert response.status_code == 200
        assert static.ADD_SNMP_CONFIG_SUC in response_content
        assert static.FIELD_REQUIRED not in response_content

    def test_post_invalid_snmp_config(self, test_user):
        self.client.force_login(test_user)
        invalid_test_data = dict(
            group_name=static.VALID_GROUP_NAME,
            snmp_user=static.VALID_SNMP_USER,
            snmp_password=static.INVALID_SNMP_PASSWORD,
            snmp_encrypt_key=static.VALID_SNMP_ENCRYPT_KEY,
            snmp_host=static.INCORRECT_NETWORK_IP,
            snmp_auth_protocol=static.VALID_SNMP_AUTH_PROTOCOL,
            snmp_privacy_protocol=static.VALID_SNMP_PRIVACY_PROTOCOL,
            server_location=static.VALID_SERVER_LOCATION,
            contact_details=static.INVALID_CONTACT_DETAILS,
            add_snmp_config=static.VALID_ADD_SNMP_CONFIG
        )

        response = self.client.post(self.path, data=invalid_test_data)
        received_content = response.content.decode('utf-8')
        assert response.status_code == 200
        assert static.ENTER_AT_LEAST_8_CHARS in received_content
        assert static.ENTER_VALID_IP in received_content
        assert static.ENTER_VALID_EMAIL in received_content
        assert static.ADD_SNMP_CONFIG_SUC not in received_content
