#  +-------------------------------------------------------+
#  | Copyright (c)ftb bank, 2023.                          |
#  +-------------------------------------------------------+
#  | NAME : SOY DARA                                     |
#  | EMAIL: soydara168@gmail.com                       |
#  | DUTY : FTB BANK (HEAD OFFICE)                         |
#  +-------------------------------------------------------+
#  | Released 22.08.2023.                                   |
#  +-------------------------------------------------------+
from ..eleave.leave_type.models import LeaveTypeModel
from ..user_management.models import Module
from django.contrib.auth import get_user_model
import random
import string
import datetime
from .DoUpload import doUploadFiles, removeUploadedByName
from ..branch.models import Branch
from ..position.models import Position
from django.db.models import Q
from django.conf import settings
from app.user_management.models import UserAvatar

User = get_user_model()


class GlobalHelper:
    @staticmethod
    def find_user_info_by_user_id(user_id):
        info = User.objects.filter(id=user_id).get()

        if info:
            position_nam_en = (
                info.position.name_en if info.position and info.position.name_en else ""
            )
            department_nam_en = (
                info.department.name_en
                if info.department and info.department.name_en
                else ""
            )
            branch_nam_en = (
                info.branch.name_en if info.branch and info.branch.name_en else ""
            )

            data = {
                "user_id": info.id,
                "staff_id": info.staff_id,
                "full_name": info.fullname,
                "first_name": info.first_name,
                "last_name": info.last_name,
                "position": position_nam_en,
                "department": department_nam_en,
                "email": info.email,
                "branch": branch_nam_en,
                "gender": info.gender,
            }
            return data

        else:
            return None

    @staticmethod
    def find_branch_by_branch_id(branch_id):
        try:
            data = Branch.objects.filter(id=branch_id).first()
            return data
        except Branch.DoesNotExist:
            return None

    @staticmethod
    def find_branch_by_branch_name(branch_name):
        try:
            data = Branch.objects.filter(name_en=branch_name).first()
            return data
        except Branch.DoesNotExist:
            return None

    @staticmethod
    def find_position_by_position_id(position_id):
        try:
            data = Position.objects.filter(id=position_id).first()
            return data
        except Position.DoesNotExist:
            return None

    @staticmethod
    def find_position_by_position_name(position_name):
        try:
            data = Position.objects.filter(name_en=position_name).first()
            return data
        except Position.DoesNotExist:
            return None

    @staticmethod
    def find_module_by_name(module_name):
        try:
            data = Module.objects.filter(module_name=module_name).first()
            return data
        except Module.DoesNotExist:
            return None

    @staticmethod
    def find_module_by_id(module_id):
        try:
            data = Module.objects.filter(id=module_id).first()
            return data
        except Module.DoesNotExist:
            return None

    @staticmethod
    def increase_user_unread_noti(user_id):
        try:
            user = User.objects.get(id=user_id)
            user.noti_count += 1
            user.save()
            return user.noti_count
        except User.DoesNotExist:
            return None

    @staticmethod
    def decrease_user_unread_noti(user_id):
        try:
            user = User.objects.get(id=user_id)
            if user.noti_count > 0:
                user.noti_count -= 1
                user.save()
            return user.noti_count
        except User.DoesNotExist:
            return None

    @staticmethod
    def find_leave_type_by_id(leave_type_id):
        try:
            data = LeaveTypeModel.objects.filter(id=leave_type_id).first()
            return data
        except LeaveTypeModel.DoesNotExist:
            return None

    @staticmethod
    def find_leave_type_by_hook_name(HOOK_KEY):
        try:
            data = LeaveTypeModel.objects.filter(HOOK_KEY=HOOK_KEY).first()
            return data
        except LeaveTypeModel.DoesNotExist:
            return None

    @staticmethod
    def generate_referent_number(prefix=""):
        date_part = datetime.datetime.now().strftime("%Y%m%d")
        timestamp_part = datetime.datetime.now().strftime("%H%M%S")
        random_chars = "".join(
            random.choices(string.ascii_uppercase + string.digits, k=4)
        )

        referent_number = f"{prefix}-{date_part}-{timestamp_part}-{random_chars}"
        return referent_number

    @staticmethod
    def do_upload_files(attachments, file_path):
        if attachments and file_path:
            get_do_upload = doUploadFiles(attachments, file_path)
            return get_do_upload
        else:
            return False

    @staticmethod
    def remove_upload_files(file_path, file_name):
        if file_path and file_name:
            do_remove = removeUploadedByName(file_path, file_name)
            return do_remove
        else:
            return False

    @staticmethod
    def find_users_by_department(department_id: int):
        users = User.objects.filter(department_id=department_id)
        user_data = [{"id": user.id, "username": user.username} for user in users]
        return {"user_by_department": user_data}

    @staticmethod
    def find_users_by_branch(branch_id: int):
        users = User.objects.filter(branch_id=branch_id)
        user_data = [{"id": user.id, "username": user.username} for user in users]
        return {"user_by_branch": user_data}


    # ----------------------------------
    # @author: Pho Khaing
    # @date: 12-12-2023
    # @param: return user name en
    # ----------------------------------
    @staticmethod
    def show_user_fullname_en_by_username(username):
        try:
            user_info = User.objects.get(username=username)
            return f"{user_info.last_name} {user_info.first_name}"

        except User.DoesNotExist:
            return None

    # ----------------------------------
    # @author: Pho Khaing
    # @date: 12-12-2023
    # @param: return user name en
    # ----------------------------------
    @staticmethod
    def show_user_fullname_en(user_id):
        try:
            user_info = User.objects.get(id=user_id)
            return f"{user_info.last_name} {user_info.first_name}"

        except User.DoesNotExist:
            return None

    # ----------------------------------
    # @author: Pho Khaing
    # @date: 12-12-2023
    # @param: return user name kh
    # ----------------------------------
    def show_user_fullname_kh(user_id):
        try:
            user_info = User.objects.get(id=user_id)
            return f"{user_info.last_name_kh} {user_info.first_name_kh}"

        except User.DoesNotExist:
            return None

    # ----------------------------------
    # @author: Pho Khaing
    # @date: 12-12-2023
    # @param: return branch name en
    # ----------------------------------
    @staticmethod
    def show_branch_name_en(branch_id):
        try:
            branch_info = Branch.objects.filter(id=branch_id).first()
            return branch_info.name_en
        except Branch.DoesNotExist:
            return None

    # ----------------------------------
    # @author: Pho Khaing
    # @date: 12-12-2023
    # @param: return branch name kh
    # ----------------------------------
    @staticmethod
    def show_branch_name_kh(branch_id):
        try:
            branch_info = Branch.objects.filter(id=branch_id).first()
            return branch_info.name_kh
        except Branch.DoesNotExist:
            return None

    # ----------------------------------
    # @author: Soy Dara
    # @date: 10-01-2024
    # @param: find user avatar
    # ----------------------------------
    @staticmethod
    def find_user_avatar_by_user_id(user_id):
        avatar_url = None
        try:
            user_avatar = UserAvatar.objects.get(user_id=user_id)
            avatar_url = f"{settings.GET_MEDIA_URL}/{user_avatar.file_path}/{user_avatar.upload_file_name}"
            return avatar_url
        except UserAvatar.DoesNotExist:
            pass
