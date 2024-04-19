from django import forms
from django.db import models
from django_filters import CharFilter, BooleanFilter
from django_filters import rest_framework as filters

from .models import LeaveBalance


class LeaveBalanceFilter(filters.FilterSet):
	class Meta:
		model = LeaveBalance
		fields = (
			"id",
			"employee",
			"start_date",
			"end_date",
			"year",
			"entitle_balance",
			"additional_balance",
			"forward_balance",
			"begin_annual_leave",
			"taken_annual_leave",
			"current_annual_leave",
			"begin_sick_leave",
			"taken_sick_leave",
			"current_sick_leave",
			"begin_special_leave",
			"taken_special_leave",
			"current_special_leave",
			"begin_maternity_leave",
			"taken_maternity_leave",
			"current_maternity_leave",
			"begin_unpaid_Leave",
			"taken_unpaid_leave",
			"current_unpaid_leave",
			"created_by",
			"created_at",
		)
