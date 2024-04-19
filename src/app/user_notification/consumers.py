from channels.generic.websocket import AsyncWebsocketConsumer
import json


class NotificationConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		self.user_id = self.scope['url_route']['kwargs']['user_id']
		self.room_group_name = f'notifications_{self.user_id}'
		
		await self.channel_layer.group_add(
			self.room_group_name,
			self.channel_name
		)
		
		await self.accept()
	
	async def disconnect(self, close_code):
		await self.channel_layer.group_discard(
			self.room_group_name,
			self.channel_name
		)
	
	async def receive(self, text_data):
		text_data_json = json.loads(text_data)
		message = text_data_json['message']
		
		await self.channel_layer.group_send(
			self.room_group_name,
			{
				'type': 'send_notification',
				'message': message
			}
		)
	
	async def send_notification(self, event):
		message = event['message']
		
		await self.send(text_data=json.dumps({
			'message': message
		}))
