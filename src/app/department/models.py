from django.db import models


class Department(models.Model):
    name_en = models.CharField(max_length=100, null=False, blank=True)
    name_kh = models.CharField(max_length=100, null=False, blank=True)
    parent = models.IntegerField(null=True, blank=True)
    segment = models.CharField(max_length=500, null=True, blank=True)
    description = models.TextField(blank=True, null=True, max_length=500)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "ftb_department"
        managed = True
        verbose_name = "Department"
        verbose_name_plural = "Departments"

    def __str__(self):
        return self.name_en
