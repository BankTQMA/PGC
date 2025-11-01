from django.contrib import admin
from .models import GradeResult

# Register your models here.


@admin.register(GradeResult)
class GradeResultAdmin(admin.ModelAdmin):
    list_display = ("id", "total_gpa", "grade_letter", "created_at")
    ordering = ("-created_at",)
    admin.site.site_header = "PGC Login"
    admin.site.site_title = "PGC Login"
    admin.site.site_title = "PGC Login"

