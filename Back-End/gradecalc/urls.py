from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("calculate/post/", views.calculate_grade_post, name="calculate_post"),
    path("my-history/", views.my_history, name="my_history"),
    path("whatif/", views.what_if, name="what_if"),
    path("auth/register/", views.register_user, name="register_user"),
    path("summary/", views.gpa_summary, name="gpa_summary"),
]

urlpatterns += [
    path("auth/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
