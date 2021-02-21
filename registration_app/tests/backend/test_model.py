import pytest
from django.contrib.auth.models import User


@pytest.fixture
def test_user():
    return User.objects.create_user(username='pytest_user', email='pytest_user@gmail.com',
                                    password='pytest_password')


@pytest.mark.run(order=1)
@pytest.mark.django_db(transaction=True)
def test_transaction_true_db_fixture(test_user):
    assert isinstance(test_user, User)


@pytest.mark.django_db(transaction=True)
@pytest.mark.run(order=2)
class TestUserModel:
    def test_user_creation(self, test_user):
        assert isinstance(test_user, User)
        assert test_user.username == 'pytest_user'
        assert test_user.email == 'pytest_user@gmail.com'
        assert isinstance(test_user.password, str)
