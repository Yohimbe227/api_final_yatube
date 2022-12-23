from typing import Any

from django.db.models.query import QuerySet
from rest_framework import viewsets, serializers, filters
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.serializers import BaseSerializer
from rest_framework.pagination import LimitOffsetPagination

from api.permissions import AccesDeniedPermissions
from api.serializers import CommentSerializer, GroupSerializer, PostSerializer, \
    FollowSerializer
from posts.models import Comment, Group, Post, Follow, User


class PostViewSet(viewsets.ModelViewSet):

    permission_classes = [
        AccesDeniedPermissions,
        IsAuthenticatedOrReadOnly,
    ]

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer: BaseSerializer[Any]) -> None:
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):

    permission_classes = [AccesDeniedPermissions, IsAuthenticatedOrReadOnly]

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = None

    def get_post(self) -> Post:
        return get_object_or_404(Post, pk=self.kwargs.get('post_id'))

    def get_queryset(self) -> QuerySet[Any]:
        return self.get_post().comments.all()

    def perform_create(self, serializer: BaseSerializer[Any]) -> None:
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
    serializer_class = FollowSerializer
    pagination_class = None
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)
    queryset = Follow.objects.all()

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer: BaseSerializer[Any]) -> None:
        # serializer.is_valid(raise_exception=True)
        serializer.save(
            user=self.request.user,
            author=get_object_or_404(User, username=serializer.initial_data.get('following'))
        )
