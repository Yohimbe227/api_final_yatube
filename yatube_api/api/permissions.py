from typing import Any

from django.http import HttpRequest
from rest_framework import permissions

from posts.models import Post


class AccesDeniedPermissions(permissions.BasePermission):
    def has_object_permission(
        self,
        request: HttpRequest,
        view: Any,
        obj: Post,
    ) -> bool:
        """
        Разрешения, выдающиеся для пользователей.

        Допуск разрешается при безопасном методе запроса или когда текущий
        пользователь есть автор поста.

        Args:
            request: Данные из запроса.
            view: Не используется.
            obj: объект класса Post.

        Returns:
            Разрешен доступ или нет.
        """
        del view
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )
