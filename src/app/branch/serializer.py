from rest_framework import serializers

from .models import Branch


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = "__all__"
        # depth = 1
    

    def validate_code(self, value):
        if len(value) <= 5:
            raise serializers.ValidationError("Branch code must greater than 5 characters!")
        return value

    # validate all fields
    def validate(self, data):
        if (len(data.get('name_en')) <= 5):
            raise serializers.ValidationError(
                "Branch name en must be 5 characters!")

        return data
