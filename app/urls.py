from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SignupView, CustomLoginView, UserProfileViewSet, LogoutView, TransactionListCreateAPIView


router = DefaultRouter()
router.register(r'userprofile', UserProfileViewSet, basename='custom-userprofile')

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', include(router.urls)),
    path('transactions/', TransactionListCreateAPIView.as_view(), name='transactions'),
]
