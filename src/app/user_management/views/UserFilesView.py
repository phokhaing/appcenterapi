#
#   +-------------------------------------------------------+
#   | Copyright (c)ftb bank.                          |
#   +-------------------------------------------------------+
#   | NAME : SOY DARA                                       |
#   | EMAIL: soydara168@gmail.com                           |
#   | DUTY : FTB BANK (HEAD OFFICE)                         |
#   | ROLE : Software Developer                             |
#   +-------------------------------------------------------+
#   | Released: Copyright (c)  5/12/2023.
#   +-------------------------------------------------------+
#
#

from django.db import transaction
from rest_framework.exceptions import ValidationError
from ...utils.DoUpload import removeUploadedByName, doUploadFiles
from ..serializer import UserAvatarSerializer
from ..models import UserAvatar


class UserFilesView():
	# --------------------------------------------------------------------------
	#  Method for update Identification File
	# --------------------------------------------------------------------------
	def update_ideFile(self, ideFiles, new_data):
		serializer = UserAvatarSerializer(ideFiles, data=new_data, partial=True)
		if serializer.is_valid():
			serializer.save()
			return serializer
		else:
			raise ValidationError({"attachment_files": serializer.errors})
	
	# --------------------------------------------------------------------------
	
	#  Method for Create Identification File
	# --------------------------------------------------------------------------
	def create_ideFile(self, identification):
		serializer_file = UserAvatarSerializer(data=identification)
		if serializer_file.is_valid():
			serializer_file.save()
			return serializer_file
		else:
			raise ValidationError({"attachment_files": serializer_file.errors})
	
	# --------------------------------------------------------------------------
	
	#  Method for create new data of identification files
	# --------------------------------------------------------------------------
	@transaction.atomic
	def create_user_files(self, files_data, user, instance):
		user_logged = user.id
		if instance:
			pathStore = f'images/profile'
			getUploaded = doUploadFiles(files_data, pathStore)
			file_serializer_list = []
			for file in getUploaded:
				file['user_id'] = instance.id
				file['created_by'] = user_logged
				file['updated_by'] = None
				# identification['description'] =  getUploaded[0]['description']
				identification_serializer = self.create_ideFile(file)
				file_serializer_list.append(identification_serializer.data)
			return file_serializer_list
		else:
			return []
	
	# --------------------------------------------------------------------------
	#  Method for create new, update and remove data of identifications files
	# --------------------------------------------------------------------------
	def update_user_files(self, file_data, new_files, user, instance):
		user_id = user.id or None
		cid = instance.id
		# Get the customer display ID Ex:CUS0000001, CUS0000002...
		cdId = instance.id
		
		if instance and cid:
			# Get the Model existing identification files
			userFiles = UserAvatar.objects.filter(user_id=cid)
			files_serializers = []
			# Create sets to store the identification file identifiers
			request_file_ids = set(file.get('id') for file in file_data)
			# Identify data for update, new, and delete
			dataUpdate = userFiles.filter(id__in=request_file_ids)
			dataDelete = userFiles.exclude(id__in=request_file_ids)
			# Perform actions for dataUpdate, dataNew, and dataDelete
			for index, modelFile in enumerate(dataUpdate):
				file_data[index]['updated_by'] = user_id
				# file_data[index]['description'] = file_data[0]['description']
				updateFileSerializer = self.update_ideFile(modelFile, file_data[index])
				files_serializers.append(updateFileSerializer)
			
			# handle removal of identificationFiles
			for item_delete in dataDelete:
				path = item_delete.file_path
				file = item_delete.upload_file_name
				item_delete.delete()
				removeUploadedByName(path, file)
			
			# Create new identification files from getUploaded
			pathStoreFile = f'images/profile'
			getUploaded = doUploadFiles(new_files, pathStoreFile)
			for new_file in getUploaded:
				if not new_file.get('id'):
					new_file['user_id'] = cid
					new_file['created_by'] = user_id
					new_file['updated_by'] = user_id
					# new_file['description'] = file_data[0]['description']
					uploadedFileSerializer = self.create_ideFile(new_file)
					files_serializers.append(uploadedFileSerializer)
			return [file.data for file in files_serializers or []]
		return []
