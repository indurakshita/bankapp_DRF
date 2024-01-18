import pytest
from django.contrib.auth.models import User
from app.models import UserProfile, Transaction
from account.serializers import UserRegistrationSerializer, CustomLoginSerializer
from app.serializers import UserProfileSerializer, TransactionSerializer
from rest_framework.exceptions import ValidationError

@pytest.fixture
def create_user(django_user_model):
    def _create_user(username='testuser', password='testpassword'):
        return django_user_model.objects.create_user(username=username, password=password)

    return _create_user


@pytest.fixture
def create_user_profile(create_user):
    def _create_user_profile(user=None, account_number='12345', balance=1000.00):
        if user is None:
            user = create_user()
        return UserProfile.objects.create(user=user, account_number=account_number, balance=balance)

    return _create_user_profile


@pytest.fixture
def create_transaction(create_user_profile):
    def _create_transaction(account=None, amount=50.00, transaction_type='deposit'):
        if account is None:
            account = create_user_profile()
        return Transaction.objects.create(account=account, amount=amount, transaction_type=transaction_type)

    return _create_transaction


@pytest.mark.django_db
def test_user_registration_serializer():
    data = {'username': 'newuser', 'password': 'newpassword'}
    serializer = UserRegistrationSerializer(data=data)

    assert serializer.is_valid()
    user = serializer.save()
    assert user.username == 'newuser'
    assert User.objects.filter(username='newuser').exists()


@pytest.mark.django_db
@pytest.mark.parametrize("data, expected_error", [
    ({'username': 'ab', 'password': 'newpassword'}, 'username'),
    ({'username': 'user@name', 'password': 'newpassword'}, 'username'),
    ({'username': 'existinguser', 'password': 'newpassword'}, 'username'),
])
def test_user_registration_serializer_invalid_data(data, expected_error):
    User.objects.create_user(username='existinguser', password='password123')
    serializer = UserRegistrationSerializer(data=data)

    assert not serializer.is_valid()
    assert expected_error in serializer.errors
   

@pytest.mark.django_db
def test_custom_login_serializer(create_user):
    # Valid credentials
    user_valid = create_user(username='testuser', password='testpassword')
    data_valid = {'username': 'testuser', 'password': 'testpassword'}
    serializer_valid = CustomLoginSerializer(data=data_valid)

    assert serializer_valid.is_valid()
    validated_data_valid = serializer_valid.validated_data
    assert validated_data_valid['username'] == 'testuser'
    assert validated_data_valid['password'] == 'testpassword'

    # Invalid credentials
    user_invalid = create_user(username='testuser2', password='testpassword2')
    data_invalid = {'username': 'testuser2', 'password': 'wrongpassword'}
    serializer_invalid = CustomLoginSerializer(data=data_invalid)

    with pytest.raises(ValidationError, match='Invalid login credentials.'):
        serializer_invalid.is_valid(raise_exception=True)

    
    
@pytest.mark.django_db
def test_user_profile_serializer(create_user_profile):
    user_profile = create_user_profile()
    serializer = UserProfileSerializer(user_profile)

    assert serializer.data['username'] == user_profile.user.username
    assert serializer.data['account_number'] == user_profile.account_number
    assert float(serializer.data['balance']) == user_profile.balance


@pytest.mark.django_db
def test_transaction_serializer(create_user_profile, create_transaction):
    user_profile = create_user_profile()
    transaction = create_transaction(account=user_profile)
    serializer = TransactionSerializer(transaction)

    assert serializer.data["username"] == user_profile.user.username
    assert float(serializer.data["amount"]) == transaction.amount
    assert serializer.data['transaction_type'] == transaction.transaction_type
    assert 'timestamp' in serializer.data