from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class GradeResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_gpa = models.FloatField()
    major_gpa = models.FloatField(null=True, blank=True)
    grade_letter = models.CharField(max_length=2)

    def __str__(self):
        return f"GPA {self.total_gpa:.2f} ({self.grade_letter})"
