from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import GradeResult, SubjectRecord
from .serializers import CalculateSerializer, WhatIfSerializer, GradeResultSerializer


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
    ser = CalculateSerializer(data=request.data)
    ser.is_valid(raise_exception=True)
    subjects = ser.validated_data["subjects"]
    total = sum(s["score"] * s["credit"] for s in subjects)
    credits = sum(s["credit"] for s in subjects)
    avg = total / credits if credits else 0
    letter = score_to_grade(avg)
    gpa4 = letter_to_gpa4(letter)
    result = GradeResult.objects.create(
        owner=request.user if request.user.is_authenticated else None,
        total_score_weighted=avg,
        gpa4=gpa4,
        grade_letter=letter,
    )
    SubjectRecord.objects.bulk_create(
        [
            SubjectRecord(
                result=result, name=s["name"], score=s["score"], credit=s["credit"]
            )
            for s in subjects
        ]
    )
    return Response(
        {"GPA_percent": round(avg, 2), "Grade": letter, "GPA_4": gpa4, "id": result.id}
    )


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
