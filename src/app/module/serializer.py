from rest_framework import serializers

from .models import Module


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = "__all__"
        depth = 1
    

    def validate_code(self, value):
        if len(value) != 9:
            raise serializers.ValidationError("Module code must 9 characters!")
        return value

    # validate all fields
    def validate(self, data):
        if (len(data.get('name_en')) < 5):
            raise serializers.ValidationError(
                "Module name en must be 9 characters!")

        return data
