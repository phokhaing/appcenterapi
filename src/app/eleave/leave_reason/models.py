from django.db import models
from django.contrib.auth import get_user_model
import uuid

# Create your models here.

User = get_user_model()


class LeaveReasonModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reason_en = models.CharField(
        max_length=500, null=False, blank=True, unique=True)
    reason_kh = models.CharField(
        max_length=500, null=False, blank=True, unique=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="%(class)s_created_by",
        null=True,
        blank=True,
        db_column="created_by",
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="%(class)s_updated_by",
        null=True,
        blank=True,
        db_column="updated_by",
    )

    class Meta:
        db_table = "ftb_eleave_leave_reason"
        managed = True
        verbose_name = "Leave Reason"
        verbose_name_plural = "Leave Reason"

    def __str__(self):
        return self.reason_en
