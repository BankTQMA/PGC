from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import User

# Create your models here.


class GradeResult(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    total_score_weighted = models.FloatField(default=0.0)
    grade_letter = models.CharField(max_length=2)
    gpa4 = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.total_score_weighted:.2f}% ({self.grade_letter})"


class SubjectRecord(models.Model):
    result = models.ForeignKey(
        GradeResult, on_delete=models.CASCADE, related_name="subjects"
    )
    name = models.CharField(max_length=100)
    score = models.FloatField()
    credit = models.FloatField()
