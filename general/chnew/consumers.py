import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone

from .models import Room, RoomMember, Message


class ChatConsumer(AsyncWebsocketConsumer):
    """
    WS URL пример: ws://host/ws/chat/<room_id>/
    (если делаешь token в querystring — user должен быть уже в scope через middleware)
    """

    async def connect(self):
        self.room_id = int(self.scope["url_route"]["kwargs"]["room_id"])
        self.group_name = f"room_{self.room_id}"
        
        await self.accept()

        user = self.scope.get("user")
        if not user or not user.is_authenticated:
            # 4401 = custom "unauthorized"
            await self.close(code=4401)
            return

        # комната существует?
        room_exists = await self.room_exists(self.room_id)
        if not room_exists:
            await self.close(code=4404)
            return

        # пользователь член комнаты?
        is_member = await self.is_room_member(self.room_id, user.id)
        if not is_member:
            await self.close(code=4403)  # forbidden
            return

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        

        # отправим историю (последние 50)
        history = await self.get_last_messages(self.room_id, limit=50)
        await self.send_json({
            "type": "history",
            "room_id": self.room_id,
            "messages": history,
        })

    async def disconnect(self, close_code):
        # safe even if not added
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        if not text_data:
            return

        user = self.scope["user"]

        try:
            payload = json.loads(text_data)
        except json.JSONDecodeError:
            await self.send_json({"type": "error", "detail": "Invalid JSON"})
            return

        event_type = payload.get("type")

        # 1) обычное сообщение
        if event_type == "message":
            text = (payload.get("text") or "").strip()
            if not text:
                return

            # ещё раз можно проверить членство (на случай если удалили из комнаты во время коннекта)
            is_member = await self.is_room_member(self.room_id, user.id)
            if not is_member:
                await self.close(code=4403)
                return

            msg_dict = await self.create_message(room_id=self.room_id, sender_id=user.id, text=text)

            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "chat.message",         # CALLS chat_message handler with event dict as argument
                    "message": msg_dict,
                }
            )
            return

        # 2) typing (в БД не пишем)
        if event_type == "typing":
            is_typing = bool(payload.get("is_typing", False))
            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "chat.typing",        # CALLS chat_typing handler with event dict as argument
                    "user_id": user.id,
                    "is_typing": is_typing,
                }
            )
            return

        await self.send_json({"type": "error", "detail": "Unknown event type"})

    # ====== group handlers ======

    async def chat_message(self, event):
        await self.send_json({
            "type": "message",
            "room_id": self.room_id,
            "message": event["message"],
        })

    async def chat_typing(self, event):
        # можно не слать typing самому себе
        if event.get("user_id") == self.scope["user"].id:
            return
        await self.send_json({
            "type": "typing",
            "room_id": self.room_id,
            "user_id": event["user_id"],
            "is_typing": event["is_typing"],
        })

    # ====== helpers ======

    async def send_json(self, data: dict):
        await self.send(text_data=json.dumps(data, ensure_ascii=False))

    @database_sync_to_async
    def room_exists(self, room_id: int) -> bool:
        return Room.objects.filter(id=room_id).exists()

    @database_sync_to_async
    def is_room_member(self, room_id: int, user_id: int) -> bool:
        return RoomMember.objects.filter(room_id=room_id, user_id=user_id).exists() or Room.objects.filter(id=room_id, owner_id=user_id).exists() # владелец или учатник

    @database_sync_to_async
    def create_message(self, room_id: int, sender_id: int, text: str) -> dict:
        msg = Message.objects.create(
            room_id=room_id,
            sender_id=sender_id,
            text=text,
        )
        return {
            "id": msg.id,
            "room_id": msg.room_id,
            "sender_id": msg.sender_id,
            "text": msg.text,
            "created_at": msg.created_at.isoformat(),
        }

    @database_sync_to_async    
    def get_last_messages(self, room_id: int, limit: int = 50) -> list[dict]:
        # ordering у тебя "-created_at", поэтому берём последние limit и потом разворачиваем для нормального порядка
        qs = (
            Message.objects
            .filter(room_id=room_id)
            .select_related("sender")
            .order_by("-created_at")[:limit]
        )
        messages = list(qs)
        messages.reverse()

        return [
            {
                "id": m.id,
                "room_id": m.room_id,
                "sender_id": m.sender_id,
                "text": m.text,
                "created_at": m.created_at.isoformat(),
            }
            for m in messages
        ]