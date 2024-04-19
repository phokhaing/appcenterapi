# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Type(models.Model):
    title = models.CharField(max_length=50, null=False)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = "ftb_epa_type"

    def __str__(self):
        return self.title


class Template(models.Model):
    title = models.CharField(max_length=100, null=False)
    type = models.ForeignKey(Type, on_delete=models.SET_NULL, null=True)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = "ftb_epa_template"

    def __str__(self):
        return self.title


class Appraisal(models.Model):
    template = models.ForeignKey(
        Template, on_delete=models.SET_NULL, null=True, db_column="template"
    )
    appraisee = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="appraisee",
        db_column="appraisee",
    )
    appraiser = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="appraiser",
        db_column="appraiser",
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="appraisal_created_by",
        db_column="created_by",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="appraisal_updated_by",
        db_column="updated_by",
    )
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = "ftb_epa_appraisal"

    def __str__(self):
        return self.active
