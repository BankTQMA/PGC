from django.contrib import admin
from .models import GradeResult, SubjectRecord

# Register your models here.

admin.site.site_header = "PGC Login"
admin.site.site_title = "Login | PGC"


class SubjectRecordInline(admin.TabularInline):
    model = SubjectRecord
    extra = 0


class GradeResultAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "total_gpa",
        "grade_letter",
        "gpa4",
        "semester",
        "year",
        "owner",
        "created_at",
    )
    ordering = ("-created_at",)
    inlines = [SubjectRecordInline]
