#  | NAME : SOY DARA                                             |
#  | EMAIL: soydara168@gmail.com                                 |
#  | PARAM : Email sending inbound and outbound                  |
#  +-------------------------------------------------------------+
#  | Released 21.JUNE.2023.                                      |
#  | VERSION : V1                                                |
#  +-------------------------------------------------------------+
from django.conf import settings
from django.core.mail import EmailMessage, get_connection
from django.core.mail import EmailMultiAlternatives
from ..user_notification.models import EmailHook, EmailTemplate
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_email_inbound(subject, body, to_email):
	context = {
		'body': body,
	}
	html_body = render_to_string("email_template/template1.html", context)
	email = EmailMultiAlternatives(
		subject=subject,
		from_email=settings.DEFAULT_FROM_EMAIL_1,
		to=[to_email]
	)
	email.attach_alternative(html_body, "text/html")
	connection = get_connection(
		host=settings.EMAIL_HOST_1,
		port=settings.EMAIL_PORT_1,
		username=settings.EMAIL_HOST_USER_1,
		password=settings.EMAIL_HOST_PASSWORD_1,
		use_tls=settings.EMAIL_USE_TLS_1,
	)
	email.connection = connection
	email.send(fail_silently=False)


def send_email_outbound(subject, body, to_email):
	# email = EmailMessage(
	#     subject=subject,
	#     body=body,
	#     to=[to_email],
	#     from_email=settings.DEFAULT_FROM_EMAIL_2,
	# )
	
	email = EmailMultiAlternatives(subject=subject, body=body, to=[to_email], from_email=settings.DEFAULT_FROM_EMAIL_2)
	
	email.attach_alternative(body, "text/html")
	
	connection = get_connection(
		host=settings.EMAIL_HOST_2,
		port=settings.EMAIL_PORT_2,
		username=settings.EMAIL_HOST_USER_2,
		password=settings.EMAIL_HOST_PASSWORD_2,
		use_tls=settings.EMAIL_USE_TLS_2,
	)
	email.connection = connection
	email.send()


def getEmailTemplateByHook(hook_name):
	try:
		email_hook = EmailHook.objects.get(hook=hook_name)
		email_template = EmailTemplate.objects.filter(hook=email_hook).first()
		return email_template
	except EmailHook.DoesNotExist:
		return None


""""
from ..utils.EmailSending import send_email_inbound, send_email_outbound, getEmailTemplateByHook

send_email_inbound(subject, message, recipient)
send_email_outbound(subject, message, recipient)
"""
