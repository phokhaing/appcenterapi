from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Menu(models.Model):
   menu_name_en = models.CharField(max_length=255, null=False, default=None, unique=True)
   menu_name_kh = models.CharField(max_length=255, null=False, default=None, unique=True)
   menu_icon = models.CharField(max_length=100, null=False, default=None)
   module_url = models.CharField(max_length=255, null=True, default=None, db_column='module_url')

   class Meta:
      db_table = 'ftb_menu_item'
      managed = True
      verbose_name = 'Menu Item'
      verbose_name_plural = "Menu Item"

   def __str__(self):
      return self.menu_name_en


class MenuOrderable(models.Model):
   orderable = models.TextField(blank=True, null=True, default="[]")

   class Meta:
      db_table = 'ftb_menu_orderable'
      managed = True
      verbose_name = 'Menu Orderable'
      verbose_name_plural = "Menu Orderable"
