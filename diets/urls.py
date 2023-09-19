from django.urls import path
from . import views

urlpatterns = [
    path("", views.Diet.as_view()),
]
