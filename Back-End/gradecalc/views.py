from django.http import JsonResponse
from math import ceil
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CalculateSerializer
from .models import GradeResult
from django.shortcuts import render


def calculate_grade(request):
    """Calculate the GPA based on entered scores"""
    scores = request.GET.get("scores")
    credits = request.GET.get("credits")

    if not scores or not credits:
        return JsonResponse({"error": "Missing data"}, status=400)

    scores = list(map(float, scores.split(",")))
    credits = list(map(float, credits.split(",")))

    total_score = sum(s * c for s, c in zip(scores, credits))
    total_credit = sum(credits)
    gpa = total_score / total_credit

    # แปลงเป็นเกรดตัวอักษรแบบง่าย ๆ
    if gpa >= 80:
        grade = "A"
    elif gpa >= 75:
        grade = "B+"
    elif gpa >= 70:
        grade = "B"
    elif gpa >= 65:
        grade = "C+"
    elif gpa >= 60:
        grade = "C"
    elif gpa >= 55:
        grade = "D+"
    elif gpa >= 50:
        grade = "D"
    else:
        grade = "F"

    return JsonResponse({"GPA": round(gpa, 2), "Grade": grade})


def score_to_grade(score):
    if score >= 80:
        return "A"
    elif score >= 75:
        return "B+"
    elif score >= 70:
        return "B"
    elif score >= 65:
        return "C+"
    elif score >= 60:
        return "C"
    elif score >= 55:
        return "D+"
    elif score >= 50:
        return "D"
    else:
        return "F"


@api_view(["POST"])
def calculate_grade_post(request):
    serializer = CalculateSerializer(data=request.data)
    if serializer.is_valid():
        subjects = serializer.validated_data["subjects"]
        total = sum(s["score"] * s["credit"] for s in subjects)
        credits = sum(s["credit"] for s in subjects)
        gpa = total / credits if credits else 0
        grade = score_to_grade(gpa)
        GradeResult.objects.create(total_gpa=gpa, grade_letter=grade)
        return Response({"GPA": round(gpa, 2), "Grade": grade})
    return Response(serializer.errors, status=400)


def input_page(request):
    if request.method == "POST":
        scores = request.POST.get("scores")
        credits = request.POST.get("credits")
        try:
            scores = list(map(float, scores.split(",")))
            credits = list(map(float, credits.split(",")))
            total = sum(s * c for s, c in zip(scores, credits))
            gpa = total / sum(credits)
            grade = (
                "A"
                if gpa >= 80
                else (
                    "B+"
                    if gpa >= 75
                    else (
                        "B"
                        if gpa >= 70
                        else (
                            "C+"
                            if gpa >= 65
                            else (
                                "C"
                                if gpa >= 60
                                else "D+" if gpa >= 55 else "D" if gpa >= 50 else "F"
                            )
                        )
                    )
                )
            )
            GradeResult.objects.create(total_score_weighted=gpa, grade_letter=grade)
            return render(
                request, "gradecalc/input.html", {"gpa": round(gpa, 2), "grade": grade}
            )
        except Exception as e:
            return render(request, "gradecalc/input.html", {"error": str(e)})
    return render(request, "gradecalc/input.html")


def history_page(request):
    results = GradeResult.objects.all().order_by("-created_at")
    return render(request, "gradecalc/history.html", {"results": results})
