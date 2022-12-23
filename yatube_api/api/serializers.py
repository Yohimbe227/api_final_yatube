import base64

from django.core.files.base import ContentFile
from django.db import models
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from posts.models import Comment, Post, Group, Follow, User


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'title', 'description', 'slug')


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Post
        fields = ('id', 'author', 'text', 'pub_date', 'image', 'group',)
        read_only_fields = ('author',)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'created', 'post')
        model = Comment
        read_only_fields = ('author', 'post',)


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
        # default=serializers.CurrentUserDefault(),
    )
    following = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        # read_only=True,
        slug_field='username',
        # default=serializers.CurrentUserDefault(),
    )

    class Meta:
        fields = ('user', 'following',)
        model = Follow
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'following'),
                name='unique_user_following',
            ),
        ]

    def validate_following(self, data):
        if data == self.request.user:
            raise serializers.ValidationError('Нельзя подписаться на себя!')
        return data
