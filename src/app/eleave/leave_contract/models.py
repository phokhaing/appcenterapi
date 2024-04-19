from django.db import models
from django.contrib.auth import get_user_model
from ..leave_type.models import LeaveTypeModel

User = get_user_model()


class LeaveContractModel(models.Model):
    name = models.CharField(max_length=255, null=False, blank=True)
    day_start = models.IntegerField(default=1, null=False, blank=False)
    month_start = models.IntegerField(default=1, null=False, blank=False)
    day_end = models.IntegerField(default=31, null=False, blank=False)
    month_end = models.IntegerField(default=12, null=False, blank=False)

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="%(class)s_created_by",
        blank=True,
        null=True,
        db_column="created_by",
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="%(class)s_updated_by",
        blank=True,
        null=True,
        db_column="updated_by",
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    status = models.BooleanField(default=True)

    default_leave_type = models.ForeignKey(
        LeaveTypeModel,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        db_column="default_leave_type",
    )

    class Meta:
        db_table = "ftb_eleave_leave_contract"
        managed = True
        verbose_name = "Leave Contract"
        verbose_name_plural = "Leave Contract"

    def __str__(self):
        return self.name
