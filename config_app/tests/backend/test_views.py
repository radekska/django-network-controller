import pytest
from django.test import Client
from django.contrib.auth.models import User


@pytest.fixture
def test_user() -> User:
    return User.objects.create_user(username='pytest_user', email='pytest_user@gmail.com',
                                    password='pytest_password')


@pytest.mark.django_db(transaction=True)
@pytest.mark.run(order=9)
class TestConfigView:
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
