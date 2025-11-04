from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import GradeResult, SubjectRecord
from .serializers import CalculateSerializer, WhatIfSerializer, GradeResultSerializer
from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.http import JsonResponse

jwt_authenticator = JWTAuthentication()


def jwt_login_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        try:
            # พยายาม authenticate ด้วย JWT จาก Header
            user_auth_tuple = jwt_authenticator.authenticate(request)
            if user_auth_tuple is not None:
                request.user, _ = user_auth_tuple
            else:
                # ไม่มี JWT ใน Header ก็ไม่เป็นไร ให้ frontend ตรวจเอง
                raise AuthenticationFailed()
        except AuthenticationFailed:
            # ถ้าเป็น request ปกติ (HTML) -> ให้ render ได้ปกติ
            if request.headers.get("Accept", "").startswith("text/html"):
                return view_func(request, *args, **kwargs)

            # ถ้าเป็น API call (JSON) -> ต้องล็อกอิน
            return JsonResponse({"detail": "Authentication required."}, status=401)

        return view_func(request, *args, **kwargs)

    return _wrapped_view


# ---------- หน้าเว็บ ----------
def login_view(request):
    return render(request, "registration/login.html")


@jwt_login_required
def index_view(request):
    return render(request, "index.html")


@jwt_login_required
def record_view(request):
    return render(request, "record.html")


@jwt_login_required
def history_view(request):
    return render(request, "history.html")


# ---------- ฟังก์ชันคำนวณเกรด ----------
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
@permission_classes([IsAuthenticated])
def calculate_grade_post(request):
    serializer = CalculateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    subjects = serializer.validated_data["subjects"]
    semester = serializer.validated_data["semester"]
    year = serializer.validated_data["year"]

    total_weighted = 0
    total_credits = 0

    for subject in subjects:
        if not subject["components"]:
            return Response(
                {
                    "detail": f"No components found in subject '{subject['subject_name']}'"
                },
                status=400,
            )

        weighted_score = sum(
            comp["score"] * (comp["weight"] / 100) for comp in subject["components"]
        )
        total_weighted += weighted_score * subject["credit"]
        total_credits += subject["credit"]

    avg = total_weighted / total_credits if total_credits else 0
    letter = score_to_grade(avg)
    gpa4 = letter_to_gpa4(letter)

    result = GradeResult.objects.create(
        owner=request.user if request.user.is_authenticated else None,
        total_gpa=avg,
        gpa4=gpa4,
        grade_letter=letter,
        semester=semester,
        year=year,
    )

    SubjectRecord.objects.bulk_create(
        [
            SubjectRecord(
                result=result,
                name=sub.get("subject_name") or sub.get("name"),
                score=sum(
                    comp["score"] * (comp["weight"] / 100) for comp in sub["components"]
                ),
                credit=sub["credit"],
            )
            for sub in subjects
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
    scale = [
        (4.0, 80),
        (3.5, 75),
        (3.0, 70),
        (2.5, 65),
        (2.0, 60),
        (1.5, 55),
        (1.0, 50),
        (0.0, 0),
    ]
    for gpa, pct in scale:
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
    User.objects.create_user(username=username, password=password)
    return Response({"message": "user created"})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def gpa_summary(request):
    user = request.user
    results = GradeResult.objects.filter(owner=user)

    if not results.exists():
        return Response({"average_percent": 0, "average_gpa4": 0, "total_subjects": 0})

    total_score = sum(r.total_gpa for r in results)
    total_gpa4 = sum(r.gpa4 for r in results)
    count = results.count()

    avg_percent = round(total_score / count, 2)
    avg_gpa4 = round(total_gpa4 / count, 2)

    return Response(
        {
            "average_percent": avg_percent,
            "average_gpa4": avg_gpa4,
            "total_subjects": count,
        }
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def gpa_tracking(request):
    results = GradeResult.objects.filter(owner=request.user).order_by("created_at")
    return Response(
        [
            {
                "id": r.id,
                "date": r.created_at.strftime("%Y-%m-%d"),
                "total_gpa": round(r.total_gpa, 2),
                "gpa4": round(r.gpa4, 2),
                "grade_letter": r.grade_letter,
                "semester": r.semester,
                "year": r.year,
            }
            for r in results
        ]
    )
