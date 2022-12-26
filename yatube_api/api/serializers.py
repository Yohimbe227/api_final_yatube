import base64

from django.core.files.base import ContentFile
from posts.models import Comment, Follow, Group, Post, User
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'title', 'description', 'slug')


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data: str) -> ContentFile:
        """
        Конвертируем строку в картинку.

        Args:
            data: строка в base64 формате.

        Returns:
            Сконвертированная из строки картинка.
        """
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Post
        fields = (
            'id',
            'author',
            'text',
            'pub_date',
            'image',
            'group',
        )
        read_only_fields = ('author',)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        fields = ('id', 'text', 'author', 'created', 'post')
        model = Comment
        read_only_fields = (
            'author',
            'post',
        )


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
    )

    class Meta:
        fields = (
            'user',
            'following',
        )
        model = Follow
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'following'],
                message='Одной подписки достаточно',
            ),
        ]

    def validate_following(self, data: str) -> str:
        """
        Проверка подписки на самого себя.

        Args:
            data: Пользователь, на которого подписываемся.

        Returns:
            Пользователь, на которого подписываемся.

        Raises:
             ValidationError: Нельзя подписаться на себя!
        """
        user = None
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            user = request.user
        if data == user:
            raise serializers.ValidationError('Нельзя подписаться на себя!')
        return data
