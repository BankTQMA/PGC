from django.urls import path
from . import views

urlpatterns = [
    path("calculate/", views.calculate_grade, name="calculate_grade"),
]
