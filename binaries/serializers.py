from rest_framework import serializers
import json

from .models import Binary

class BinarySerializer(serializers.Serializer):
    key = serializers.CharField()
    value = serializers.CharField()

    def create(self, validated_data):
        if Binary.objects.filter(key=validated_data['key']):
            b = Binary.objects.update(**validated_data)
        else:
            b = Binary.objects.create(**validated_data)
        return b

    def delete(self, validated_data):
        Binary.objects.filter(key=validated_data['key']).delete()
        return validated_data['key']

    def validate_key(self, value):
        data = {
            "detail": [
                "This field is required."
            ]
        }
        if value:
            return value
        else:
            raise serializers.ValidationError(json.dumps(data))
