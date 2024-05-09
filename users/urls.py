from rest_framework import routers
from .views import UserRegister, MyTokenObtainPairView, VerifyTokenView, TestView, UserList
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
urlpatterns = [
    path('', include(router.urls)),

    path('register/', UserRegister.as_view(), name='register'),
    path('login/', MyTokenObtainPairView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify/', VerifyTokenView.as_view(), name='token_verify'),
    path('admin/create_user/', UserRegister.as_view(), name='admin-create-user'),
    path('test/', TestView.as_view(), name='test'),
    path('users/', UserList.as_view(), name='user-list'),

]