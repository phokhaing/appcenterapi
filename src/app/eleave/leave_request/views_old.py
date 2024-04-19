from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .filter import LeaveRequestFilter
from .serializer import LeaveRequestSerializer
from .models import LeaveRequest
from ..leave_type.models import LeaveTypeModel
from ..leave_file.serializer import LeaveFileSerializer
from django.db import transaction
from django.contrib.auth import get_user_model

User = get_user_model()

import datetime
from ...utils.UserAccessPermission import permission_required
from ...utils.DoUpload import removeUploadedByName, doUploadFiles

# block import **** Notification and Email Setting ******
from django.conf import settings
from ...utils.GlobalHelper import GlobalHelper
from ...utils.EmailSending import send_email_inbound, send_email_outbound, getEmailTemplateByHook
from ...utils import NotificationSending
from ...user_notification.models import Notification
from ...user_notification.serializer import NotificationStoreSerializer

# End block import **** Notification and Email Setting ******

module_name = "ELEAVE/LEAVE_REQUEST"


class LeaveRequestPagination(PageNumberPagination):
	page_size = 10
	page_size_query_param = "page_size"


def calculate_minutes(hour):
	# Convert the hour to a datetime object
	time = datetime.datetime.strptime(hour, "%H")
	# Calculate the minutes
	minutes = time.hour * 60 + time.minute
	return minutes


class UploadFilesView():
	@transaction.atomic
	def upload_items(self, attachment, user, instance, user_logged):
		if instance:
			pathStore = f'eleave/attachment/staff_id/{user}/{instance}'
			getUploaded = doUploadFiles(attachment, pathStore)
			file_serializer_list = []
			
			for file in getUploaded:
				file['leave_id'] = instance
				file['created_by'] = user_logged
				file['status'] = 1
				file_serializer_list.append(file)
				serializer_file = LeaveFileSerializer(data=file)
				if serializer_file.is_valid():
					serializer_file.save()
			
			return file_serializer_list
		else:
			return []


class LeaveRequestViewSet(viewsets.ModelViewSet):
	queryset = LeaveRequest.objects.all()
	serializer_class = LeaveRequestSerializer
	
	pagination_class = LeaveRequestPagination
	filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
	
	fields = ("id", "staff_id", "staff_name")
	ordering_fields = fields  # ordering by field name
	search_fields = fields  # search by field name
	filterset_class = LeaveRequestFilter
	
	@permission_required(module_name, "LIST")
	def list(self, request, *args, **kwargs):
		return Response(status=405)
	
	@transaction.atomic
	@permission_required(module_name, "CREATE")
	def create(self, request, *args, **kwargs):
		
		user_logged = request.user  # current user login
		
		# employee = get_infor_single_user(int(request.data['employee']))
		employee = GlobalHelper.find_user_info_by_user_id(int(request.data.get('employee')[0]))  # print('employee': ['1'])
		
		if not employee:
			return Response({"error": "Invalid employee information"}, status=status.HTTP_400_BAD_REQUEST)
		
		module_data = GlobalHelper.find_module_by_name("ELEAVE/LEAVE_REQUEST")
		if not module_data:
			return Response({"error": "Invalid module name"}, status=status.HTTP_400_BAD_REQUEST)
		
		email_template = getEmailTemplateByHook('ELEAVE_HOOK')  # get hook email
		if not email_template:
			return Response({"error": "Invalid email template"}, status=status.HTTP_400_BAD_REQUEST)
		
		start_date = datetime.datetime.strptime(request.data['start_date'], '%d-%m-%Y').strftime('%Y-%m-%d')
		end_date = datetime.datetime.strptime(request.data['end_date'], '%d-%m-%Y').strftime('%Y-%m-%d')
		
		incharge_request = 'N'
		incharge_certifier = 'N' if request.data.get('incharge_certifier') == 'false' else 'Y'
		incharge_authorizer = 'N' if request.data.get('incharge_authorizer') == 'false' else 'Y'
		
		hour = request.data['hours']
		minute = request.data['minute']
		
		convert_hour_to_minute = calculate_minutes(hour)
		total_time = convert_hour_to_minute + int(minute)
		
		certifier = GlobalHelper.find_user_info_by_user_id(request.data['certifier'])
		authorizer = GlobalHelper.find_user_info_by_user_id(request.data['authorizer'])
		
		# ********** for view test data get value *************#
		context = {
			'user_id': employee['user_id'],  # information of user request take leave
			'staff_id': employee['staff_id'],
			'staff_name': employee['full_name'],
			'staff_position': employee['position'].name_en,
			'staff_department': employee['department'].name_en,
			'leave_type': request.data['leave_type'],
			'start_date': start_date,
			'end_date': end_date,
			'from_time': request.data['from_time'],
			'to_time': request.data['to_time'],
			'hours': request.data['hours'],
			'minute': minute,
			'total_time': total_time,
			'certifier': certifier['user_id'],
			'authorizer': authorizer['user_id'],
			'incharge_request': incharge_request,
			'incharge_certifier': incharge_certifier,
			'incharge_authorizer': incharge_authorizer,
			'reason': request.data['reason'],
			'status': 1,  # requested
			'requested_by': user_logged.id,
			'requested_at': datetime.datetime.now(),
			'created_by': user_logged.id,
		}
		
		# print("context:", context)
		# return False
		
		serializer = LeaveRequestSerializer(data=context)
		if serializer.is_valid():
			instance = serializer.save()
			
			# #****** Do upload files ******#
			if 'attachment_files_upload' in request.data:
				files = request.data['attachment_files_upload']
				if files:
					attachment = request.FILES.getlist("attachment_files_upload") or []
					staff_id = employee['staff_id']
					upload_files = UploadFilesView()
					upload_files.upload_items(attachment, staff_id, instance.id, user_logged.id)
			# #****** End Do upload files ******#
			
			# #****** Send Notification ******#
			# module_data = GlobalHelper.find_module_by_name("ELEAVE/LEAVE_REQUEST")
			# Extend the dictionaries before appending to data_users
			extended_certifier = certifier.copy() if certifier else {}
			extended_authorizer = authorizer.copy() if authorizer else {}
			
			# Extend data to json
			if extended_certifier:
				extended_certifier['status'] = 'certify'
			if extended_authorizer:
				extended_authorizer['status'] = 'authorize'
			
			data_users = []
			# data_users.append(certifier)
			# data_users.append(authorizer)
			
			data_users.append(extended_certifier)
			data_users.append(extended_authorizer)
			
			if data_users:
				for user in data_users:
					# save notification to table database
					noti_message = 'has been send request leave to you.'
					data_notification = {
						"from_user": employee['user_id'],  # user requested
						"to_user": user['user_id'],  # to user by id
						"url": 'admin/home',  # url click to access link route (insert your frontend route)
						"message": noti_message,  # message send to notification
						"record_id": instance.id,  # recode id (input your primary key row data)
						"module_id": module_data.id,  # module id (input your moduleID)
						"is_read": False,  # unread
					}
					# print("data_notification:", data_notification)
					
					serializer_notification = NotificationStoreSerializer(data=data_notification)
					if serializer_notification.is_valid():
						serializer_notification.save()
						
						# increase unread notification by user
						unread_count = GlobalHelper.increase_user_unread_noti(user['user_id'])
						
						# message = unread_count  # return count unread to client
						message = {
							'total_unread': unread_count,
							'message': employee['full_name'] + " " + noti_message + " " + user['status'],
						}
						
						# print("message:", message)
						NotificationSending.send_notification_to_user(user['user_id'], message)
						
						# *** Send Mail *** #
						# email_template = getEmailTemplateByHook('ELEAVE_HOOK')  # get hook email
						if email_template:
							template_title = email_template.title
							template_message = email_template.message
							message_body = {
								"[NAME]": user['first_name'] + ' ' + user['last_name'],
								"[FIRST_NAME]": employee['first_name'],
								"[LAST_NAME]": employee['last_name'],
								"[SITE_URL]": 'my-site/loan/test/email',
								"[SITE_NAME]": settings.SITE_NAME,
								"[STATUS]": user['status'],
							}
							# Create a copy of the template message
							user_template_message = template_message
							# Replace the keywords in the user-specific message
							for keyword, replacement in message_body.items():
								user_template_message = user_template_message.replace(keyword, replacement)
							# send email inbound configuration
							send_email_inbound(template_title, user_template_message, user['email'])
						# send_email_outbound(template_title, user_template_message, user['email'])
			else:
				return Response({"error": "Invalid users"}, status=status.HTTP_400_BAD_REQUEST)
			return Response({'message': 'Leave request has been created'}, status=status.HTTP_201_CREATED)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	
	@permission_required(module_name, "VIEW")
	def retrieve(self, request, *args, **kwargs):
		return Response(status=405)
	
	@permission_required(module_name, "UPDATE")
	def update(self, request, *args, **kwargs):
		return Response(status=405)
	
	@permission_required(module_name, "UPDATE")
	def partial_update(self, request, *args, **kwargs):
		return Response(status=405)
	
	@permission_required(module_name, "DELETE")
	def destroy(self, request, *args, **kwargs):
		return Response(status=405)


def get_manager_from_user(user_id):
	instance = User.objects.filter(username=user_id).first()
	if instance:
		data = {
			'user_id': instance.id,
			'staff_id': instance.staff_id,
			'first_name': instance.first_name,
			'last_name': instance.last_name,
			'fullname': f"{instance.first_name} {instance.last_name}",
			'manager': instance.manager.username if instance.manager else None,
		}
		return data
	else:
		return []


class FetchUserCertifyAuthorize(APIView):
	def get(self, request):
		user_logged = request.user
		certify = get_manager_from_user(user_logged.manager)
		authorize = get_manager_from_user(certify['manager'])
		
		context = {
			"certify": certify,
			"authorize": authorize,
		}
		# print("context:", context)
		return Response(
			{
				"success": True,
				"status": status.HTTP_200_OK,
				"message": "success",
				"data": context,
			}
		)
