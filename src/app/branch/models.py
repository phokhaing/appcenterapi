from django.db import models


class Branch(models.Model):
    # code = models.CharField(max_length=255, null=False, unique=True)
    code = models.CharField(max_length=255, null=False)
    name_en = models.CharField(max_length=100, blank=True, null=True)
    name_kh = models.CharField(max_length=100, blank=True, null=True)
    address_en = models.TextField(blank=True, null=True, max_length=500)
    address_kh = models.TextField(blank=True, null=True, max_length=500)
    description = models.TextField(blank=True, null=True, max_length=500)
    is_active = models.BooleanField(default=True, blank=True, null=True)

    class Meta:
        db_table = "ftb_branch"
        managed = True
        verbose_name = "Branch"
        verbose_name_plural = "Branches"

    def __str__(self):
        return self.name_en
