from django.http import JsonResponse
from math import ceil


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
