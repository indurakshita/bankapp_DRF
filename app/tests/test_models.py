import pytest
from django.contrib.auth.models import User
from app.models import UserProfile, Transaction

@pytest.fixture
def create_user():
    def _create_user(username='testuser', password='testpassword'):
        return User.objects.create_user(username=username, password=password)
    return _create_user

@pytest.fixture
def create_user_profile(create_user):
    def _create_user_profile(user=None, account_number='12345', balance=1000.00):
        if user is None:
            user = create_user()
        return UserProfile.objects.create(user=user, account_number=account_number, balance=balance)
    return _create_user_profile

@pytest.mark.django_db
def test_user_profile_creation(create_user_profile):
    user_profile = create_user_profile()
    assert UserProfile.objects.count() == 1
    assert user_profile.user.username == 'testuser'
    assert str(user_profile) == "testuser's Profile"

@pytest.mark.django_db
def test_transaction_creation(create_user_profile):
    user_profile = create_user_profile()
    transaction_data = {'amount': 50.00, 'transaction_type': 'deposit'}
    transaction = Transaction.objects.create(account=user_profile, **transaction_data)
    
    assert Transaction.objects.count() == 1
    assert transaction.account == user_profile
    assert transaction.amount == 50.00
    assert transaction.transaction_type == 'deposit'
    assert 'deposit' in str(transaction) 

@pytest.mark.django_db
def test_user_profile_str_representation(create_user_profile):
    user_profile = create_user_profile()
    assert str(user_profile) == "testuser's Profile"

@pytest.mark.django_db
def test_transaction_str_representation(create_user_profile):
    user_profile = create_user_profile()
    transaction_data = {'amount': 50.00, 'transaction_type': 'deposit'}
    transaction = Transaction.objects.create(account=user_profile, **transaction_data)
    assert 'deposit' in str(transaction)
