from django.urls import path
from . import views

urlpatterns = [
    path("calculate/", views.calculate_grade, name="calculate_grade"),
    path("calculate/post/", views.calculate_grade_post, name="calculate_post"),
    path("result/", views.list_results, name="list_results")
]
