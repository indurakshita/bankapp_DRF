import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from rest_framework import status
from app.models import Transaction, UserProfile



@pytest.fixture
def authenticated_user():
    user = User.objects.create_user(username='testuser', password='testpass')
    return user

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_token(authenticated_user):
    return Token.objects.create(user=authenticated_user)

@pytest.fixture
def subscription(authenticated_user):
    return User.objects.create(user=authenticated_user, plan='Basic')

@pytest.fixture
def authenticated_client(authenticated_user):
    client = APIClient()
    client.force_authenticate(user=authenticated_user)
    return client

@pytest.fixture
def create_user_profile(authenticated_user):
    return UserProfile.objects.create(user=authenticated_user, account_number='test123')

@pytest.fixture
def create_transaction(create_user_profile):
    user_profile = create_user_profile
    return Transaction.objects.create(account=user_profile, amount=100, transaction_type='deposit')

@pytest.fixture
def authenticated_client(authenticated_user):
    client = APIClient()
    user = authenticated_user
    client.force_authenticate(user=user)
    return client


# Tests
@pytest.mark.django_db
def test_signup_view(api_client):
    url = reverse('signup')
    data = {'username': 'testuser', 'password': 'testpass'}
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.django_db
def test_signup_view_invalid_data(api_client):
    url = reverse('signup')
    invalid_data = {'username': 'ch', 'password': 'chan'}
    response = api_client.post(url, invalid_data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_custom_login_view_authenticated_user(api_client, authenticated_user):
    url = reverse('login')
    data = {'username': authenticated_user.username, 'password': 'testpass'}
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_302_FOUND
    assert response.url == reverse('custom-userprofile-list')

@pytest.mark.django_db
def test_custom_login_view_invalid_credentials(api_client):
    url = reverse('login')
    data = {'username': 'nonexistentuser', 'password': 'wrongpassword'}
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
def test_custom_login_view_authenticated_user_with_token(api_client, authenticated_user, create_token):
    token = create_token
    url = reverse('login')
    data = {'token': str(token)}
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_custom_login_view_invalid_token(api_client):
    url = reverse('login')
    data = {'token': 'invalid-token'}
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
def test_logout_view(authenticated_client):
    url = reverse('logout')
    response = authenticated_client.post(url, follow=True)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_list_user_profile_authenticated(authenticated_client, create_user_profile):
    url = reverse('custom-userprofile-list')
    response = authenticated_client.get(url)
    assert response.status_code == status.HTTP_200_OK



# Tests for TransactionListCreateAPIView
@pytest.mark.django_db
def test_create_transaction(authenticated_client, create_user_profile):
    url = reverse('transactions') 
    data = {'amount': 100, 'transaction_type': 'deposit'}
    response = authenticated_client.post(url, data)
    assert response.status_code == status.HTTP_302_FOUND 

  

