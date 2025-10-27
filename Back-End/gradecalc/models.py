from django.db import models

# Create your models here.


class GradeResult(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    total_score_weighted = models.FloatField(default=0.0)
    grade_letter = models.CharField(max_length=2)

    def __str__(self):
        return f"{self.total_score_weighted:.2f}% ({self.grade_letter})"
