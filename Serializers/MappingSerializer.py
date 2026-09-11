from rest_framework import serializers
from Apps.Mapping.models import Mapping


class MappingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Mapping
        fields = [
            "id",
            "doctor",
            "patient",
            "created_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_by", "created_at", "updated_at"]