from django.db import models
from django.contrib.auth import get_user_model
from ..leave_type.models import LeaveTypeModel

User = get_user_model()


class LeaveRequestStatus(models.Model):
	name = models.CharField(max_length=255, blank=True, null=True)
	created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='%(class)s_created_by', blank=True, null=True, db_column='created_by')
	updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='%(class)s_updated_by', blank=True, null=True, db_column='updated_by')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	
	def __str__(self):
		return self.name
	
	class Meta:
		db_table = 'ftb_eleave_leave_status'
		managed = True
		verbose_name = 'Leave status'
		verbose_name_plural = 'Leave status'


class LeaveRequest(models.Model):
	user_id = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='user_id', null=True)  # user request leave
	staff_id = models.CharField(max_length=255, blank=True, null=True)
	staff_name = models.CharField(max_length=255, blank=True, null=True)
	staff_position = models.CharField(max_length=255, blank=True, null=True)
	staff_department = models.CharField(max_length=255, blank=True, null=True)
	leave_type = models.ForeignKey(LeaveTypeModel, on_delete=models.SET_NULL, related_name='leave_type', null=True)  # request leave type
	start_date = models.DateField(blank=True, null=True)  # start date from leave
	end_date = models.DateField(blank=True, null=True)  # end data from leave
	duration = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)  # total day (not use)
	# from_time = models.TimeField(blank=True, null=True)  # from time
	from_time = models.CharField(max_length=255, blank=True, null=True)
	# to_time = models.TimeField(blank=True, null=True)  # to time
	to_time = models.CharField(max_length=255, blank=True, null=True)
	hours = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)  # leave hour
	minute = models.IntegerField(blank=True, null=True)  # leave minute
	total_time = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)  # total time
	reason = models.TextField(blank=True, null=True)  # leave reason
	# user request submitted
	requested_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='%(class)s_requested_by', blank=True, null=True, db_column='requested_by')
	requested_at = models.DateTimeField(blank=True, null=True)
	certifier = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='%(class)s_certifier', blank=True, null=True,
	                              db_column='certifier')  # user request selected certifier
	certifier_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='%(class)s_certifier_by', blank=True, null=True,
	                                 db_column='certifier_by')  # user real certified
	certifier_at = models.DateTimeField(blank=True, null=True)  # user real certified at
	authorizer = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='%(class)s_authorizer', blank=True, null=True,
	                               db_column='authorizer')  # user request selected authorizer
	authorizer_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='%(class)s_authorizer_by', blank=True, null=True,
	                                  db_column='authorizer_by')  # user real authorized
	authorizer_at = models.DateTimeField(blank=True, null=True)  # user real authorized at
	#  authorizer rejected
	rejected_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='%(class)s_rejected_by', blank=True, null=True, db_column='rejected_by')
	rejected_at = models.DateTimeField(blank=True, null=True)
	rejected_reason = models.TextField(blank=True, null=True)
	#  authorizer cancelled
	canceled_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='%(class)s_canceled_by', blank=True, null=True, db_column='canceled_by')
	canceled_at = models.DateTimeField(blank=True, null=True)
	canceled_reason = models.TextField(blank=True, null=True)
	#  incharge
	incharge_request = models.CharField(max_length=5, blank=True, null=True)  # user request checkbox Incharge
	incharge_certifier = models.CharField(max_length=5, blank=True, null=True)  # user request checkbox Incharge certifier
	incharge_authorizer = models.CharField(max_length=5, blank=True, null=True)  # user request checkbox Incharge authorizer
	created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='%(class)s_created_by', blank=True, null=True, db_column='created_by')
	updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='%(class)s_updated_by', blank=True, null=True, db_column='updated_by')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	""""
	status::1=Planned,2=Requested,3=Accepted,4=Rejected,5=Cancellation,6=Canceled,7=Authorized
	"""
	leave_status = models.ForeignKey(LeaveRequestStatus, on_delete=models.SET_NULL, related_name='leave_status', null=True)
	
	# status = models.IntegerField(
	# 	blank=True,
	# 	null=True,
	# 	help_text="<u>Satus:</u> 1=requested,2=certified,3=authorized,4=rejected,5=pending,6=..."
	# )
	
	def __str__(self):
		return self.staff_name
	
	def formatted_datetime(self):
		return self.requested_at.strftime('%Y-%m-%d %H:%M:%S')
	
	class Meta:
		db_table = 'ftb_eleave_leave_request'
		managed = True
		verbose_name = 'Leave request'
		verbose_name_plural = 'Leave request'
