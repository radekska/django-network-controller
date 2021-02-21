import pytest
from django.test import Client


@pytest.mark.django_db(transaction=True)
@pytest.mark.run(order=2)
class TestBackendView:
    def setup_method(self):
        self.client = Client()
        self.path = '/registration/'

    def test_get_request(self):
        response = self.client.get(path=self.path)
        assert response.status_code == 200

    def test_post_request(self):
        registration_data = dict(
            username='test_user_view',
            password1='test_password_view'
        )
        response = self.client.post(path=self.path, data=registration_data)
        assert response.status_code == 200
