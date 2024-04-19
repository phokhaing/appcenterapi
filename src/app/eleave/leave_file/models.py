from django.db import models
from ..leave_request.models import LeaveRequest
from django.contrib.auth import get_user_model

User = get_user_model()


class LeaveFile(models.Model):
    leave_id = models.ForeignKey(LeaveRequest, on_delete=models.CASCADE, db_column="leave_id", related_name='leave_files')
    upload_file_name = models.CharField(max_length=500, blank=True, null=True)
    original_name = models.CharField(max_length=500, blank=True, null=True)
    file_type = models.CharField(max_length=255, blank=True, null=True)
    extension = models.CharField(max_length=12, blank=True, null=True)
    file_size = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.IntegerField(blank=True, null=True)
    file_path = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="%(class)s_created_by",
        blank=True,
        null=True,
        db_column="created_by",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="%(class)s_updated_by",
        blank=True,
        null=True,
        db_column="updated_by",
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "ftb_eleave_leave_file"
        verbose_name = "Leave file"
        verbose_name_plural = "Leave files"
        managed = True
