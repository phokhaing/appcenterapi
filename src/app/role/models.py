from django.db import models


class Role(models.Model):
    role_name_en = models.CharField(max_length=100, null=False, unique=True)
    role_name_kh = models.CharField(max_length=100, null=False, unique=True)
    description = models.TextField(blank=True, max_length=500)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "ftb_role"
        managed = True
        verbose_name = "Role"
        verbose_name_plural = "Roles"

    def __str__(self):
        return self.role_name_en
