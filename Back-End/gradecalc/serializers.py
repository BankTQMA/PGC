from rest_framework import serializers
from .models import GradeResult, SubjectRecord


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectRecord
        fields = ["name", "score", "credit"]


class GradeResultSerializer(serializers.ModelSerializer):
    subjects = SubjectSerializer(many=True, read_only=True)

    class Meta:
        model = GradeResult
        fields = [
            "id",
            "total_score_weighted",
            "gpa4",
            "grade_letter",
            "created_at",
            "subjects",
        ]


class CalculateSerializer(serializers.Serializer):
    subjects = SubjectSerializer(many=True)


class WhatIfSerializer(serializers.Serializer):
    target_gpa4 = serializers.FloatField(min_value=0, max_value=4)
