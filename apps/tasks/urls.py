from django.urls import path
from apps.tasks import views

urlpatterns = [
    path("hello", views.hello_world),
    path("hello-json", views.HelloView.as_view()),
]
