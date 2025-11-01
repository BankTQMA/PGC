from django.contrib import admin
from .models import GradeResult, SubjectRecord

# Register your models here.


class SubjectRecordInline(admin.TabularInline):
    model = SubjectRecord
    extra = 0


@admin.register(GradeResult)
class GradeResultAdmin(admin.ModelAdmin):
    list_display = ("id", "total_gpa", "grade_letter", "gpa4", "created_at", "owner")
    ordering = ("-created_at",)
    inlines = [SubjectRecordInline]
