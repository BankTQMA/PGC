from django.contrib import admin
from .models import GradeResult, SubjectRecord

# Register your models here.

admin.site.site_header = "PGC Login"
admin.site.site_title = "Login | PGC"


class SubjectRecordInline(admin.TabularInline):
    model = SubjectRecord
    extra = 0


@admin.register(GradeResult)
class GradeResultAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "owner",
        "semester",
        "year",
        "total_gpa",
        "grade_letter",
        "created_at",
    )
    list_filter = ("semester", "year", "owner")
    search_fields = ("owner__username", "semester", "year", "grade_letter")
    ordering = ("-created_at",)


class SubjectRecordAdmin(admin.ModelAdmin):
    list_display = ("id", "result", "name", "credit", "score")
    search_fields = ("name",)
    ordering = ("id",)
