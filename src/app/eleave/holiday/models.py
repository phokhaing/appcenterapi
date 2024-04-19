from django.db import models
from django.contrib.auth import get_user_model
from ..leave_contract.models import LeaveContractModel
User = get_user_model()


class HolidayModel(models.Model):
    type = models.CharField(max_length=100, null=True, blank=True)
    title =  models.CharField(max_length=128, null=True, blank=True)
    date = models.DateField(null=False, blank=True , unique=True, help_text="<u>Date value could not be duplicate.</u>")
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    # Leave Contract Foreign key 
    default_leave_contract = models.ForeignKey(
        LeaveContractModel,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        db_column="default_leave_contract",
    )
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
    class Meta:
        db_table = 'ftb_eleave_dayoffs'
        managed = True
        verbose_name = "Holiday"
        verbose_name_plural = "Holidays"


    def __str__(self):
        return self.title
    
class WeekendModel(models.Model):
    title =  models.CharField(max_length=128, null=True, blank=True)
    days =   models.CharField(max_length=50, null=True, blank=True)
    year =   models.CharField(max_length=50, null=True, blank=True)
    mark_as = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    # Leave Contract Foreign key 
    default_leave_contract = models.ForeignKey(
        LeaveContractModel,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        db_column="default_leave_contract",
    )
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

    class Meta:
        db_table = 'ftb_eleave_weekends'
        managed = True
        verbose_name = "Weekend"
        verbose_name_plural = "Weekends"


    def __str__(self):
        return self.title
    