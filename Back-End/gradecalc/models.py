from django.db import models

# Create your models here.


class GradeResult(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    total_gpa = models.FloatField()
    grade_letter = models.CharField(max_length=2)

    def __str__(self):
        return f"GPA {self.total_gpa:.2f} ({self.grade_letter})"
