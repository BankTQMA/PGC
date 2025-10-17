from rest_framework import serializers


class SubjectSerializer(serializers.Serializer):
    name = serializers.CharField()
    score = serializers.FloatField(min_value=0, max_value=100)
    credit = serializers.FloatField(min_value=0.5, max_value=6)


class CalculateSerializer(serializers.Serializer):
    subjects = SubjectSerializer(many=True)
