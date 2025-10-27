from django.contrib import admin
from .models import GradeResult

# Register your models here.


@admin.register(GradeResult)
class GradeResultAdmin(admin.ModelAdmin):
    list_display = ("id", "total_score_weighted", "grade_letter", "created_at")
    ordering = ("-created_at",)
