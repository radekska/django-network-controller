import pytest
from django.contrib.auth.models import User

# giving pytest access to database.
pytestmark = pytest.mark.django_db


class TestUserModel:
    def setup_method(self):
        self.test_user = User.objects.create_user(username='pytest_user', email='pytest_user@gmail.com',
                                                  password='pytest_password')

    def test_user_creation(self):
        assert isinstance(self.test_user, User)
        assert self.test_user.username == 'pytest_user'
        assert self.test_user.email == 'pytest_user@gmail.com'
        assert isinstance(self.test_user.password, str)
