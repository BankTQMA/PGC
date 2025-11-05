from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("", views.index_view, name="index"),
    path("record/", views.record_view, name="record_page"),
    path("calculate/post/", views.calculate_grade_post, name="calculate_post"),
    path("my-history/", views.my_history, name="my_history"),
    path("what-if/", views.what_if, name="what_if"),
    path("auth/register/", views.register_user, name="register_user"),
    path("auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("summary/", views.gpa_summary, name="gpa_summary"),
    path("gpa-tracking/", views.gpa_tracking, name="gpa_tracking"),
    path("gpa-by-year/", views.gpa_by_year, name="gpa_by_year"),
    path("record/<int:record_id>/", views.record_detail, name="record_detail"),
]
