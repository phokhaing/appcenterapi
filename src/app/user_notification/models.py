from django.db import models
from django.conf import settings
from ..user_management.models import Module
from django.contrib.auth import get_user_model

User = get_user_model()


class Notification(models.Model):
   from_user = models.ForeignKey(
      User,
      on_delete=models.SET_NULL,
      related_name='%(class)s_from_user',
      null=True
   )
   to_user = models.ForeignKey(
      User,
      on_delete=models.SET_NULL,
      related_name='%(class)s_to_user',
      null=True
   )
   url = models.CharField(max_length=255)
   message = models.CharField(max_length=255)
   record_id = models.CharField(max_length=555, null=True, blank=True)
   module_id = models.ForeignKey(
      Module,
      on_delete=models.SET_NULL,
      related_name='module_id',
      db_column="module_id",
      null=True
   )
   is_read = models.BooleanField(default=False)
   created_at = models.DateTimeField(auto_now_add=True)

   class Meta:
      db_table = "ftb_user_notification"
      managed = True
      verbose_name = "User notification"
      verbose_name_plural = "User notifications"


class EmailHook(models.Model):
   hook = models.CharField(max_length=255, null=True, default=None)
   hook_name = models.CharField(max_length=255, null=True, default=None)
   created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='%(class)s_created_by', blank=True,
                                  null=True, db_column='created_by')
   updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='%(class)s_updated_by', blank=True,
                                  null=True, db_column='updated_by')
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)
   status = models.BooleanField(default=True)

   def __str__(self):
      return self.hook

   class Meta:
      db_table = 'ftb_email_hook'
      managed = True
      verbose_name = 'Email hook'
      verbose_name_plural = '01. Email hooks'


class EmailLanguage(models.Model):
   title = models.CharField(max_length=255, null=True, default=None)
   created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='%(class)s_created_by', blank=True,
                                  null=True, db_column='created_by')
   updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='%(class)s_updated_by', blank=True,
                                  null=True, db_column='updated_by')
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)
   status = models.BooleanField(default=True)

   def __str__(self):
      return self.title

   class Meta:
      db_table = 'ftb_email_language'
      managed = True
      verbose_name = 'Email language'
      verbose_name_plural = '02. Email languages'


class EmailTemplate(models.Model):
   title = models.CharField(max_length=255, null=True, default=None)
   message = models.TextField(blank=False)
   hook = models.ForeignKey(
      EmailHook,
      null=True,
      blank=True,
      on_delete=models.CASCADE,
      db_column='hook'
   )
   language = models.ForeignKey(
      EmailLanguage,
      null=True,
      blank=True,
      on_delete=models.CASCADE,
      db_column='language'
   )
   created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='%(class)s_created_by', blank=True,
                                  null=True, db_column='created_by')
   updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='%(class)s_updated_by', blank=True,
                                  null=True, db_column='updated_by')
   created_at = models.DateTimeField(auto_now_add=True)
   updated_at = models.DateTimeField(auto_now=True)
   status = models.BooleanField(default=True)

   class Meta:
      db_table = 'ftb_email_template'
      managed = True
      verbose_name = 'Email template'
      verbose_name_plural = '03. Email templates'
