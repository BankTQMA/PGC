from django.contrib import admin
from .models import GradeResult
from django.urls import path, include

# Register your models here.


@admin.register(GradeResult)
class GradeResultAdmin(admin.ModelAdmin):
    list_display = ("id", "total_gpa", "grade_letter", "created_at")
    ordering = ("-created_at",)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("gradecalc.urls")),
]
