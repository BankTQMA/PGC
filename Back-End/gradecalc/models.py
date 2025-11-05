from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class GradeResult(models.Model):
    # user ที่เป็นเจ้าของผลลัพธ์ (null = guest)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="results",
    )

    # ค่าเฉลี่ยแบบเปอร์เซ็นต์ (0-100)
    total_gpa = models.FloatField(default=0.0)

    # เกรดตัวอักษร เช่น A, B+, C
    grade_letter = models.CharField(max_length=2)

    # ค่าบนสเกล 4.0 เช่น 3.5
    gpa4 = models.FloatField(default=0.0)

    # ภาคเรียนและปีการศึกษา
    semester = models.CharField(max_length=10, default="1")
    year = models.IntegerField(default=2025)

    # วันที่บันทึกข้อมูล ใช้สำหรับแสดงกราฟ
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        owner_name = self.owner.username if self.owner else "Guest"
        return f"GPA {self.total_gpa:.2f} ({self.grade_letter}) - {owner_name}"

    class Meta:
        verbose_name = "Grade Calculation Result"
        verbose_name_plural = "Grade Calculation History"
        ordering = ["-created_at"]


# เก็บข้อมูลรายวิชา
class SubjectRecord(models.Model):
    result = models.ForeignKey(
        GradeResult,
        on_delete=models.CASCADE,
        related_name="subjects",
    )
    name = models.CharField(max_length=100)
    score = models.FloatField()
    credit = models.FloatField()

    def __str__(self):
        return f"{self.name} - {self.score:.2f}% ({self.credit} credits)"
