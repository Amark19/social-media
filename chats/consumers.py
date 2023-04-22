from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import Thread, ChatMessage
from django.core import serializers
import json
from datetime import datetime

User = get_user_model()


class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("connected", event)
        user = self.scope['user']
        chat_room = f'user_room_{user.id}'
        self.chat_room = chat_room
        '''
        Add the chat-room name channelslayer,chat-room acts as a group in django(anyuser can join group) but we will consider only one-one conversation i.e it will be unique for each authenticated user i.e a authenticated user can send message to any user within chat-room

        and this groups contains set of channels i.e set of users who are connected to this chat-room(in our case only one)
        '''
        await self.channel_layer.group_add(
            chat_room,
            self.channel_name
        )

        await self.send({
            "type": "websocket.accept"
        })

    async def websocket_receive(self, event):
        print("receive", event)
        data_received = json.loads(event['text'])
        msg = data_received['message']
        sender = self.scope['user']
        receiver_id = data_received['sent_to']
        thread_id = data_received['thread_id']

        if not msg:
            return False

        sender_user = await self.get_user(sender.id)
        receiver_user = await self.get_user(receiver_id)
        thread_obj = await self.get_thread(thread_id)
        thread_data  = await self.get_thread_data(thread_obj)
        
        await self.create_message( msg, thread_obj, sender_user)


        other_user_chat_room = f'user_room_{receiver_user.id}'
        res = {
            'message': msg,
            'sent_by': sender_user.id,
            'thread': json.dumps(thread_data),
        }

        # distribute this msg to other chat_room
        await self.channel_layer.group_send(
            other_user_chat_room,
            {
                "type": "chat_message",
                "text": json.dumps(res)
            }
        )

        # also distribute this msg to sender chat_room
        await self.channel_layer.group_send(
            self.chat_room,
            {
                "type": "chat_message",
                "text": json.dumps(res)
            }
        )

    async def websocket_disconnect(self, event):
        print("disconnected", event)

    async def chat_message(self, event):
        await self.send({
            "type": "websocket.send",
            "text": event['text']
        })

    @database_sync_to_async
    def get_user(self, user_id):
        user = User.objects.filter(id=user_id)
        return user.first() if user.exists() else None

    @database_sync_to_async
    def get_thread(self, thread_id):
        thread_obj = Thread.objects.filter(id=thread_id)
        thread_obj.update(timestamp=datetime.now())
        thread_obj.order_by('timestamp')
        return thread_obj.first() if thread_obj.exists() else None

    @database_sync_to_async
    def create_message(self, msg, thread_obj, user):
        return ChatMessage.objects.create(
            thread=thread_obj,
            user=user,
            message=msg,
        )
    
    @database_sync_to_async
    def get_thread_data(self, thread_obj):
        return {'thread_id':thread_obj.id, 'user1':thread_obj.user1.id, 'user2':thread_obj.user2.id,'profile1':thread_obj.user1_profile_pic.user_pic.url,'profile2':thread_obj.user2_profile_pic.user_pic.url}
