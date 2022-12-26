from typing import Any

from django.db.models.query import QuerySet
from rest_framework import filters, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.permissions import AccesDeniedPermissions
from api.serializers import (CommentSerializer, FollowSerializer,
                             GroupSerializer, PostSerializer)
from posts.models import Comment, Follow, Group, Post, User


class PostViewSet(viewsets.ModelViewSet):

    permission_classes = [
        AccesDeniedPermissions,
        IsAuthenticatedOrReadOnly,
    ]

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer: PostSerializer[Any]) -> None:
        """
        Сохраняем в поле author значение текущего пользователя.

        Args:
            serializer: сериализатор модели Post.
        """
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):

    permission_classes = [AccesDeniedPermissions, IsAuthenticatedOrReadOnly]

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = None

    def get_post(self) -> Post:
        """
        Получаем объект Post по его `id`.

        Returns:
            Объект Post.
        """
        return get_object_or_404(Post, pk=self.kwargs.get('post_id'))

    def get_queryset(self) -> QuerySet[Any]:
        """
        Переопределяем `queryset`.

        Returns:
            Все комментарии к заданному посту.
        """
        return self.get_post().comments.all()

    def perform_create(self, serializer: CommentSerializer[Any]) -> None:
        """
        Переопределяем сохрание сериализатора.

        Args:
            serializer: сериализатор `CommentSerializer`.
        """
        serializer.save(
            author=self.request.user,
            post=self.get_post(),
        )


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    pagination_class = None


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)
    pagination_class = None

    def get_queryset(self) -> None:
        """
        Переопределяем `queryset`.

        Returns:
            Все объекты подписок текущего пользователя.
        """
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer: FollowSerializer[Any]) -> None:
        """
        В поле `following` записываем значение из json запроса.

        Args:
            serializer: Сериализатор `FollowSerializer`.
        """
        serializer.save(
            user=self.request.user,
            following=get_object_or_404(
                User,
                username=serializer.initial_data.get('following'),
            ),
        )
