from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from django.core import serializers

class NotificationConsumer(AsyncJsonWebsocketConsumer):
    async def websocket_connect(self, event):
        print("CONNECTED", event)
        user = self.scope['user']
        grp = 'notifications_group_{}'.format(user.id)
        await self.accept()
        await self.channel_layer.group_add(grp, self.channel_name)
        context = await self.get_notification_info(self.scope)
        await self.send_json(content=context)

    async def websocket_disconnect(self, event):
        print("DISCONNECTED", event)

    async def websocket_receive(self, event):
        print("RECEIVE", event)
        await self.send(text_data='HELLO')

    async def notification_info(self, event):
        context = await self.get_notification_info(self.scope)
        await self.send_json(content=context)

    @database_sync_to_async
    def get_notification_info(self, scope):
        if not scope['user'].is_authenticated:
            context = {
                'unreaded_notification_count':'',
                'unreaded_notifications':'',
                'old_notifications':''
            }
            return context

        notifications = scope['user'].receiver.order_by('-created_at')
        old_notifications = notifications.filter(is_read=True)
        unreaded_notifications = notifications.filter(is_read=False).order_by('-created_at')
        context = {
            'unreaded_notification_count':unreaded_notifications.count(),
            'unreaded_notifications':serializers.serialize('json', unreaded_notifications),
            'old_notifications':serializers.serialize('json', old_notifications[:3])
        }
        return context
