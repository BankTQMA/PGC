from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import GradeResult, SubjectRecord
from .serializers import CalculateSerializer, WhatIfSerializer, GradeResultSerializer
from django.shortcuts import render
import os
from django.conf import settings
from django.shortcuts import render


def index_view(request):
    return render(request, "index.html")

def record_view(request):
    return render(request, "record.html")

def score_to_grade(score):
    if score >= 80:
        return "A"
    if score >= 75:
        return "B+"
    if score >= 70:
        return "B"
    if score >= 65:
        return "C+"
    if score >= 60:
        return "C"
    if score >= 55:
        return "D+"
    if score >= 50:
        return "D"
    return "F"


def letter_to_gpa4(letter):
    return {
        "A": 4.0,
        "B+": 3.5,
        "B": 3.0,
        "C+": 2.5,
        "C": 2.0,
        "D+": 1.5,
        "D": 1.0,
        "F": 0.0,
    }[letter]


@api_view(["POST"])
@permission_classes([AllowAny])
def calculate_grade_post(request):
    serializer = CalculateSerializer(data=request.data)
    if serializer.is_valid():
        subjects = serializer.validated_data["subjects"]
        semester_data = serializer.validated_data["semester"]
        year_data = serializer.validated_data["year"]

        total_weighted = 0
        total_credits = 0

        for subject in subjects:
            total_weighted += subject["score"] * subject["credit"]
            total_credits += subject["credit"]

        # คำนวณ GPA
        avg = total_weighted / total_credits if total_credits else 0
        letter = score_to_grade(avg)
        gpa4 = letter_to_gpa4(letter)

        # บันทึกลงฐานข้อมูล
        result = GradeResult.objects.create(
            owner=request.user if request.user.is_authenticated else None,
            total_gpa=avg,
            gpa4=gpa4,
            grade_letter=letter,
            semester=semester_data,
            year=year_data
        )

        # สร้าง SubjectRecord สำหรับแต่ละวิชา
        SubjectRecord.objects.bulk_create(
            [
                SubjectRecord(
                    result=result,
                    name=subject["name"],
                    score=subject["score"],
                    credit=subject["credit"],
                )
                for subject in subjects
            ]
        )

        return Response(
            {
                "GPA_percent": round(avg, 2),
                "Grade": letter,
                "GPA_4": gpa4,
                "id": result.id,
            }
        )
    return Response(serializer.errors, status=400)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_history(request):
    results = GradeResult.objects.filter(owner=request.user).order_by("-created_at")
    return Response(GradeResultSerializer(results, many=True).data)


@api_view(["POST"])
@permission_classes([AllowAny])
def what_if(request):
    ser = WhatIfSerializer(data=request.data)
    ser.is_valid(raise_exception=True)
    target = ser.validated_data["target_gpa4"]
    map_ = [
        (4.0, 80),
        (3.5, 75),
        (3.0, 70),
        (2.5, 65),
        (2.0, 60),
        (1.5, 55),
        (1.0, 50),
        (0.0, 0),
    ]
    for gpa, pct in map_:
        if target >= gpa:
            return Response({"target_gpa4": target, "required_avg_percent": pct})
    return Response({"target_gpa4": target, "required_avg_percent": 0})


@api_view(["POST"])
@permission_classes([AllowAny])
def register_user(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if not username or not password:
        return Response({"error": "missing credentials"}, status=400)
    if User.objects.filter(username=username).exists():
        return Response({"error": "user exists"}, status=400)
    user = User.objects.create_user(username=username, password=password)
    return Response({"message": "user created"})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def gpa_summary(request):
    qs = GradeResult.objects.filter(owner=request.user)
    if not qs.exists():
        return Response({"average_percent": 0, "average_gpa4": 0})
    avg_percent = round(sum(r.total_score_weighted for r in qs) / len(qs), 2)
    avg_gpa4 = round(sum(r.gpa4 for r in qs) / len(qs), 2)
    return Response({"average_percent": avg_percent, "average_gpa4": avg_gpa4})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def gpa_tracking(request):
    """
    Return a list of GPA records for the logged-in user,
    used for displaying progress tracking graphs.
    """
    results = GradeResult.objects.filter(owner=request.user).order_by("created_at")

    data = [
        {
            "id": r.id,
            "date": r.created_at.strftime("%Y-%m-%d"),
            "total_gpa": round(r.total_gpa, 2),
            "gpa4": round(r.gpa4, 2),
            "grade_letter": r.grade_letter,
        }
        for r in results
    ]

    return Response(data)
