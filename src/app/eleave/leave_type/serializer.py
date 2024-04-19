from rest_framework import serializers

from .models import LeaveTypeModel

from django.contrib.auth import get_user_model
User = get_user_model()

class LeaveTypeSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(default=serializers.CurrentUserDefault(), read_only=True)
    
    
    class Meta:
        model = LeaveTypeModel
        fields = "__all__"
        #depth = 1

    def validate_name(self, value):
        if len(value) <= 5:
             raise serializers.ValidationError(
                "Field name allow min lenght 5 characters!"
            )
        return value


    # Validate Duplicate Data
    # def validate_nameduplicate(self,value):
    #     name_value = value.get('name')
    #     existing_data = LeaveTypeModel.objects.filter(name = name_value)

    #     if self.instance:
    #         existing_data = existing_data.exclude(pk=self.instance.pk)

    #     if(existing_data.exists()):
    #          raise serializers.ValidationError(
    #             "Duplicate data already exists"
    #         )
    #     return value