from django.db import models


class Position(models.Model):
    name_en = models.CharField(max_length=500, null=True, blank=True)
    name_kh = models.CharField(max_length=500, null=True, blank=True)
    segment = models.CharField(max_length=500, null=True, blank=True)
    description = models.TextField(blank=True, null=True, max_length=500)
    is_active = models.BooleanField(default=True, null=True, blank=True)

    class Meta:
        db_table = 'ftb_position'
        managed = True
        verbose_name = 'Position'
        verbose_name_plural = 'Positions'

    def __str__(self):
        return self.name_en
