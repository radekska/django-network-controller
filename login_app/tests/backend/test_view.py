import pytest
from django.test import Client
from django.contrib.auth.models import User

# giving pytest access to database.
pytestmark = pytest.mark.django_db


class TestLoginView:
    def setup_method(self):
        self.client = Client()
        self.path = '/login/'

    def test_get_request(self):
        response = self.client.get(path=self.path)
        assert response.status_code == 200

    def test_post_request(self):
        login_data = dict(
            username='test_user_view',
            password='test_password_view'
        )

        response = self.client.post(path=self.path, data=login_data)
        assert response.status_code == 200

