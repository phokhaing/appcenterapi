from rest_framework import serializers

from .models import Appraisal

class AppraisalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appraisal
        fields = "__all__"
        depth = 1

    # override fun update
    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.appraisee = validated_data.get('appraisee', instance.appraisee)
        instance.appraiser = validated_data.get('appraiser', instance.appraiser)
        return instance
    
    # validate appraisee only
    def validate_appraisee(self, value):
        if value is None:
            raise serializers.ValidationError("Field appraisee must not be None!!")
        return value

    # validate appraiser only
    def validate_appraiser(self, value):
        if value is None:
            raise serializers.ValidationError("Field appraiser must not be None!!")
        return value
    
    # validate all fields
    def validate(self, data):
        if (data.get('appraisee') == data.get('appraiser')):
            raise serializers.ValidationError("Field appraisee and appraiser don't allow same value!!")
        else:
            return data

