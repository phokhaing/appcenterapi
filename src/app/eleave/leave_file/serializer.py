from rest_framework import serializers
from .models import LeaveFile
from django.conf import settings


class LeaveFileSerializer(serializers.ModelSerializer):
	url = serializers.SerializerMethodField()
	
	def get_url(self, instance):
		base_url = settings.GET_MEDIA_URL
		return f"{base_url}/{instance.file_path}/{instance.upload_file_name}"
	
	class Meta:
		model = LeaveFile
		fields = "__all__"
