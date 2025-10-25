from django.shortcuts import render
from django.http import JsonResponse
from math import ceil
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import CalculateSerializer, GradeResultSerializer
from .models import GradeResult


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
@authentication_classes([BasicAuthentication, TokenAuthentication   ])
@permission_classes([IsAuthenticated])  # <--- This is from our previous step
def calculate_grade_post(request):
    serializer = CalculateSerializer(data=request.data)
    if serializer.is_valid():
        subjects = serializer.validated_data["subjects"]
        
        calculated_subjects = [] # A new list to hold final scores

        # --- 1. First, calculate the final score for each subject ---
        for subject in subjects:
            components = subject['components']
            
            # Calculate the weighted score for this one subject
            subject_score = sum(
                (c['score'] * (c['weight'] / 100.0)) for c in components
            )
            
            # Store the calculated info
            calculated_subjects.append({
                "score": subject_score,
                "credit": subject['credit'],
                "is_major": subject.get('is_major', False)
            })

        # --- 2. Overall GPA (using calculated scores) ---
        total = sum(s["score"] * s["credit"] for s in calculated_subjects)
        credits = sum(s["credit"] for s in calculated_subjects)
        gpa = total / credits if credits else 0
        grade = score_to_grade(gpa)
        
        # --- 3. Major-only GPA (using calculated scores) ---
        major_subjects = [s for s in calculated_subjects if s['is_major']]
        
        major_total = sum(s["score"] * s["credit"] for s in major_subjects)
        major_credits = sum(s["credit"] for s in major_subjects)
        
        major_gpa = major_total / major_credits if major_credits > 0 else 0
        
        # --- 4. Save to database (no change here) ---
        GradeResult.objects.create(
            user=request.user, 
            total_gpa=gpa, 
            major_gpa=major_gpa, 
            grade_letter=grade
        ) 
        
        # --- 5. Return new response (no change here) ---
        return Response({
            "GPA": round(gpa, 2), 
            "Major_GPA": round(major_gpa, 2), 
            "Grade": grade
        })
        
    return Response(serializer.errors, status=400)

# ... (your other views) ...

@api_view(['GET'])
@authentication_classes([BasicAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_results(request):
    """
    Handles GET requests to list all grade results
    for the currently authenticated user.
    """
    # 1. Filter results to *only* get ones for the logged-in user
    results = GradeResult.objects.filter(user=request.user).order_by('-created_at')
    
    # 2. Serialize the data (many=True since it's a list)
    serializer = GradeResultSerializer(results, many=True)
    
    # 3. Return the JSON response
    return Response(serializer.data)

def index_view(request):
    """
    serve the main HTML page
    """
    return render(request, "index.html")
