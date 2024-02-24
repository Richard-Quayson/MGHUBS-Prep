from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import AccountRegistrationView, AccountLoginView, AccountView, AccountLogoutView


urlpatterns = [
    path("register/", AccountRegistrationView.as_view(), name="register"),
    path("login/", AccountLoginView.as_view(), name="login"),
    path("logout/", AccountLogoutView.as_view(), name="logout"),
    path("profile/", AccountView.as_view(), name="profile"),
    path("token/refresh/", TokenRefreshView.as_view(), name="refresh"),
]