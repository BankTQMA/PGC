from rest_framework import serializers
from .models import GradeResult, SubjectRecord


class ComponentSerializer(serializers.Serializer):
    name = serializers.CharField()
    score = serializers.FloatField(min_value=0, max_value=100)
    weight = serializers.FloatField(min_value=1, max_value=100)


class SubjectSerializer(serializers.Serializer):
    name = serializers.CharField()
    credit = serializers.FloatField(min_value=0.5, max_value=6)
    is_major = serializers.BooleanField(required=False, default=False)
    components = ComponentSerializer(many=True)

    def validate_components(self, components):
        total_weight = sum(c["weight"] for c in components)
        if total_weight != 100:
            raise serializers.ValidationError(
                f"Component weights must add up to 100, not {total_weight}."
            )
        return components


class CalculateSerializer(serializers.Serializer):
    subjects = SubjectSerializer(many=True)


class WhatIfSerializer(serializers.Serializer):
    target_gpa4 = serializers.FloatField(min_value=0, max_value=4)


class GradeResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = GradeResult
        fields = ["id", "total_gpa", "gpa4", "grade_letter", "created_at"]
