from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class GradeResult(models.Model):
    # user ที่เป็นเจ้าของผลลัพธ์ (null = guest ผู้ใช้ที่ไม่ได้ login)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="results",  # ทำให้ user.results ใช้ได้
    )

    # ค่าเฉลี่ยแบบเปอร์เซ็นต์ (0-100)
    total_gpa = models.FloatField(default=0.0)

    # เกรดตัวอักษร เช่น A, B+, C
    grade_letter = models.CharField(max_length=2)

    # ค่าบนสเกล 4.0 เช่น 3.5
    gpa4 = models.FloatField(default=0.0)

    # วันที่บันทึกข้อมูล ใช้แสดงกราฟ
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # แสดงผลสวยในหน้า Django Admin
        return f"GPA {self.total_gpa:.2f} ({self.grade_letter}) - {self.owner.username if self.owner else 'Guest'}"

    class Meta:
        verbose_name = "Grade Calculation Result"
        verbose_name_plural = "Grade Calculation History"
        ordering = ["-created_at"]  # sort ค่าใหม่สุดก่อน


# เก็บข้อมูลรายวิชาสำหรับแต่ละครั้งที่คำนวณ GPA
class SubjectRecord(models.Model):
    result = models.ForeignKey(
        GradeResult,
        on_delete=models.CASCADE,
        related_name="subjects",  # ทำให้ result.subjects.all() ใช้ได้
    )

    name = models.CharField(max_length=100)  # ชื่อวิชา
    score = models.FloatField()  # คะแนนรวมถ่วงน้ำหนักของวิชานั้น
    credit = models.FloatField()  # หน่วยกิตของวิชานั้น

    def __str__(self):
        return f"{self.name} - {self.score:.2f}% ({self.credit} credits)"
