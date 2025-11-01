from rest_framework import serializers
from .models import GradeResult, SubjectRecord

class SubjectSerializer(serializers.Serializer):
    name = serializers.CharField()
    credit = serializers.FloatField(min_value=0.5, max_value=6)
    score = serializers.FloatField(min_value=0, max_value=100)


class CalculateSerializer(serializers.Serializer):
    subjects = SubjectSerializer(many=True)
    semester = serializers.CharField()
    year = serializers.IntegerField()


class WhatIfSerializer(serializers.Serializer):
    target_gpa4 = serializers.FloatField(min_value=0, max_value=4)


class GradeResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = GradeResult
        fields = ["id", "total_gpa", "gpa4", "grade_letter", "created_at", "semester", "year"]
