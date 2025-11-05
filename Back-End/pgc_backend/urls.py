"""
URL configuration for pgc_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from gradecalc import views

urlpatterns = [
    path("", views.index_view, name="index"),
    path("login/", views.login_view, name="login_page"),
    path("register/", views.register_view, name="register_page"),
    path("add-record/", views.record_view, name="record_page"),
    path("history/", views.history_view, name="history_page"),
    path("admin/", admin.site.urls),
    path("api/", include("gradecalc.urls")),
    path("__reload__/", include("django_browser_reload.urls")),
]
