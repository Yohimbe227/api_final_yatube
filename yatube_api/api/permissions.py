from typing import Any

from django.http import HttpRequest
from posts.models import Post
from rest_framework import permissions


class AccesDeniedPermissions(permissions.BasePermission):
    def has_object_permission(
        self,
        request: HttpRequest,
        view: Any,
        obj: Post,
    ) -> bool:
        del view
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )
