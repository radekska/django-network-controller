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


@pytest.mark.django_db(transaction=True)
@pytest.mark.run(order=10)
class TestSNMPConfigView:
    def setup_method(self):
        self.client = Client()
        self.path = "/dashboard/config_network/"

    def test_get_request(self, test_user):
        self.client.force_login(test_user)
        response = self.client.get(path=self.path)
        assert response.status_code == 200

    def test_post_add_snmp_config(self, test_user):
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

    def test_snmp_configuration_list_details(self, test_user):
        self.client.force_login(test_user)
        self.test_post_add_snmp_config(test_user)
        response = self.client.get(self.path)
        received_content = response.content.decode('utf-8')
        assert static.VALID_GROUP_NAME in received_content
        assert static.VALID_SNMP_USER in received_content
        assert static.VALID_SNMP_PASSWORD in received_content
        assert static.VALID_SNMP_ENCRYPT_KEY in received_content
        assert static.VALID_SNMP_HOST in received_content
        assert static.VALID_SNMP_AUTH_PROTOCOL in received_content
        assert static.VALID_SNMP_PRIVACY_PROTOCOL in received_content
        assert static.VALID_SERVER_LOCATION in received_content
        assert static.VALID_CONTACT_DETAILS in received_content
        assert static.VALID_ADD_SNMP_CONFIG in received_content


@pytest.mark.django_db(transaction=True)
@pytest.mark.run(order=11)
class TestNetworkAutomation:
    def setup_method(self):
        self.client = Client()
        self.path = "/dashboard/config_network/"
        self.access_config_view = TestAccessConfigView()
        self.snmp_config_view = TestSNMPConfigView()

        self.access_config_view.setup_method()
        self.snmp_config_view.setup_method()

    def test_scan_network_button(self, test_user, config_id=5):
        self.client.force_login(test_user)
        self.access_config_view.test_post_add_access_config(test_user)

        scan_data = dict(
            id=config_id,
            available_hosts='Scan Network'
        )
        response = self.client.post(self.path, data=scan_data)
        received_content = response.content.decode('utf-8')

        assert response.status_code == 200
        assert static.DEVICES_AVAILABLE in received_content

    def post_request_buttons(self, test_user, button_name):
        self.client.force_login(test_user)
        self.access_config_view.test_post_add_access_config(test_user)
        self.snmp_config_view.test_post_add_snmp_config(test_user)
        self.test_scan_network_button(test_user, config_id=6)

        request_data = dict(
            id=['6', '5'],
            run_snmp_config=button_name
        )

        response = self.client.post(self.path, data=request_data)
        received_content = response.content.decode('utf-8')

        return response.status_code, received_content

    def test_configure_and_rollback_buttons(self, test_user):
        for button in static.BUTTONS:
            status_code, content = self.post_request_buttons(test_user, button)
            assert status_code == 200
            assert static.SNMP_AUTH_FAILED in content
