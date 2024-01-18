from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import  UserProfileViewSet, TransactionListCreateAPIView


router = DefaultRouter()
router.register(r'userprofile', UserProfileViewSet, basename='custom-userprofile')

urlpatterns = [

    path('api/', include(router.urls)),
    path('transactions/', TransactionListCreateAPIView.as_view(), name='transactions'),
]
