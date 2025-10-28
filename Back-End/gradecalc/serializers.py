from rest_framework import serializers
from .models import GradeResult

class ComponentSerializer(serializers.Serializer):
    """
    Validates a single weighted component, like
    {"name": "Coursework", "score": 80, "weight": 40}
    """
    name = serializers.CharField()
    score = serializers.FloatField(min_value=0, max_value=100)
    weight = serializers.FloatField(min_value=1, max_value=100)

class SubjectSerializer(serializers.Serializer):
    """
    Validates a subject, which now contains a list of components
    instead of a single score.
    """
    name = serializers.CharField()
    credit = serializers.FloatField(min_value=0.5, max_value=6)
    is_major = serializers.BooleanField(required=False, default=False)
    
    # We replaced 'score' with 'components'
    components = ComponentSerializer(many=True)

    def validate_components(self, components):
        """
        Custom validation to ensure all component weights
        for this subject add up to 100.
        """
        if not components:
            raise serializers.ValidationError("Components list cannot be empty.")
            
        total_weight = sum(c['weight'] for c in components)
        if total_weight != 100:
            raise serializers.ValidationError(f"Component weights must add up to 100, not {total_weight}.")
        return components

class CalculateSerializer(serializers.Serializer):
    subjects = SubjectSerializer(many=True)

class GradeResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = GradeResult
        fields = ['id', 'created_at', 'total_gpa', 'major_gpa', 'grade_letter']