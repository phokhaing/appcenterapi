#  send notification to user
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def send_notification_to_user(user_id, message):
	channel_layer = get_channel_layer()
	room_group_name = f'notifications_{user_id}'
	
	async_to_sync(channel_layer.group_send)(
		room_group_name,
		{
			'type': 'send_notification',
			'message': message,
		}
	)
