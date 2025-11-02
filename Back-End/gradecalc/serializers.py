from rest_framework import serializers
from .models import GradeResult, SubjectRecord


class ComponentSerializer(serializers.Serializer):
    name = serializers.CharField()
    score = serializers.FloatField(min_value=0, max_value=100)
    weight = serializers.FloatField(min_value=1, max_value=100)


class SubjectSerializer(serializers.Serializer):
    name = serializers.CharField()
    credit = serializers.FloatField(min_value=0.5, max_value=6)
    components = ComponentSerializer(many=True)

    def validate_components(self, components):
        total_weight = sum(c["weight"] for c in components)
        if abs(total_weight - 100) > 0.001:
            raise serializers.ValidationError(
                f"คะแนนส่วนประกอบต้องรวมเป็น 100% ตอนนี้ได้ {total_weight:.2f}%"
            )
        return components


class CalculateSerializer(serializers.Serializer):
    subjects = SubjectSerializer(many=True)
    semester = serializers.CharField()
    year = serializers.IntegerField()


class WhatIfSerializer(serializers.Serializer):
    target_gpa4 = serializers.FloatField(min_value=0, max_value=4)


class GradeResultSerializer(serializers.ModelSerializer):
    subjects = serializers.SerializerMethodField()

    def get_subjects(self, obj):
        return [
            {
                "name": s.name,
                "score": round(s.score, 2),
                "credit": s.credit,
            }
            for s in obj.subjects.all()
        ]

    class Meta:
        model = GradeResult
        fields = [
            "id",
            "total_gpa",
            "gpa4",
            "grade_letter",
            "semester",
            "year",
            "created_at",
            "subjects",
        ]
