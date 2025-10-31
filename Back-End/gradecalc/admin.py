from django.contrib import admin
from .models import GradeResult

# Register your models here.


@admin.register(GradeResult)
class GradeResultAdmin(admin.ModelAdmin):
    list_display = ("id", "total_gpa", "grade_letter", "created_at")
    ordering = ("-created_at",)


def __str__(self):
    return f"GPA {self.total_gpa:.2f} ({self.grade_letter}) - {self.owner.username if self.owner else 'Guest'}"
