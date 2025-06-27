from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from apps.users import views

urlpatterns = [
    path("auth/login/", views.Login.as_view(), name="login"),
    path("auth/register/", views.Register.as_view(), name="register"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("auth/me/", views.Me.as_view(), name="me"),
]
