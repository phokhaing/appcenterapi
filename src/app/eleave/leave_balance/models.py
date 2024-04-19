from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()


class LeaveBalance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="employee", null=True
    )
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)

    entitle_balance = models.FloatField(
        default=0, blank=True, null=True
    )  # total hour time duration as minute
    additional_balance = models.FloatField(
        default=0, blank=True, null=True
    )  # total hour time duration as minute
    forward_balance = models.FloatField(
        default=0, blank=True, null=True
    )  # total hour time duration as minute

    begin_annual_leave = models.FloatField(
        default=0, blank=True, null=True
    )  # total hour time duration as minute
    taken_annual_leave = models.FloatField(
        default=0, blank=True, null=True
    )  # total hour time duration as minute
    current_annual_leave = models.FloatField(
        default=0, blank=True, null=True
    )  # total hour time duration as minute

    begin_sick_leave = models.FloatField(
        default=0, blank=True, null=True
    )  # total hour time sick leave duration as minute
    taken_sick_leave = models.FloatField(
        default=0, blank=True, null=True
    )  # total hour time sick leave duration as minute
    current_sick_leave = models.FloatField(
        default=0, blank=True, null=True
    )  # total hour time sick leave duration as minute

    begin_special_leave = models.FloatField(
        default=0, blank=True, null=True
    )  # total hour time duration as minute
    taken_special_leave = models.FloatField(
        default=0, blank=True, null=True
    )  # total hour time duration as minute
    current_special_leave = models.FloatField(
        default=0, blank=True, null=True
    )  # total hour time duration as minute

    begin_maternity_leave = models.FloatField(
        default=0, blank=True, null=True
    )  # total hour time duration as minute
    taken_maternity_leave = models.FloatField(
        default=0, blank=True, null=True
    )  # total hour time duration as minute
    current_maternity_leave = models.FloatField(
        default=0, blank=True, null=True
    )  # total hour time duration as minute

    begin_unpaid_Leave = models.FloatField(
        default=0, blank=True, null=True
    )  # total hour time duration as minute
    taken_unpaid_leave = models.FloatField(
        default=0, blank=True, null=True
    )  # total hour time duration as minute
    current_unpaid_leave = models.FloatField(
        default=0, blank=True, null=True
    )  # total hour time duration as minute

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="%(class)s_created_by",
        blank=True,
        null=True,
        db_column="created_by",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="%(class)s_updated_by",
        blank=True,
        null=True,
        db_column="updated_by",
    )

    def __str__(self):
        return str(self.employee)

    class Meta:
        db_table = "ftb_eleave_leave_balance"
        managed = True
        verbose_name = "Leave balance"
        verbose_name_plural = "Leave balance"
