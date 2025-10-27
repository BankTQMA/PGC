from django.urls import path
from . import views

urlpatterns = [
    path("calculate/", views.calculate_grade, name="calculate_grade"),
    path("calculate/post/", views.calculate_grade_post, name="calculate_post"),
    path("input/", views.input_page, name="input_page"),
    path("history/", views.history_page, name="history_page"),
]
