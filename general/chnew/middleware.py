from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser

@database_sync_to_async
def get_user_from_drf_token(token: str):
    from rest_framework.authtoken.models import Token
    try:
        t = Token.objects.select_related("user").get(key=token)
        return t.user
    except Token.DoesNotExist:
        return AnonymousUser()

class DRFTokenAuthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        # если уже есть user из сессии — не трогаем
        user = scope.get("user")
        if user and getattr(user, "is_authenticated", False):
            return await self.app(scope, receive, send)

        query = parse_qs(scope.get("query_string", b"").decode())
        token = (query.get("token") or [None])[0]

        if token:
            scope["user"] = await get_user_from_drf_token(token)
        else:
            scope["user"] = AnonymousUser()

        return await self.app(scope, receive, send)
