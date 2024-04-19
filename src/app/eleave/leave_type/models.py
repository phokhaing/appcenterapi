from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class LeaveTypeModel(models.Model):
    name = models.CharField(max_length=255, null=False, blank=True, unique=True,
                            help_text="<u>Leave type name for sick leave, you must input this name for sick leave:</u> Sick Leave")
    acronym = models.CharField(max_length=255, null=True, blank=True)
    deduct_days_off = models.BooleanField(default=True)

    entitle_balance = models.FloatField(
        max_length=255, default=0)
    additional_balance = models.FloatField(
        max_length=255, default=0)
    HOOK_KEY = models.CharField(
        max_length=50, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="%(class)s_created_by",
        blank=True,
        null=True,
        db_column="created_by",
    )

    class Meta:
        db_table = "ftb_eleave_leave_type"
        managed = True
        verbose_name = "Leave Type"
        verbose_name_plural = "Leave Types"

    def __str__(self):
        return self.name
