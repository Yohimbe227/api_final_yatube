from django.contrib import admin

from posts.models import Comment, Group, Post, Follow


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'pub_date', 'author')
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'slug', 'description')
    list_editable = ('description',)
    search_fields = ('title',)
    list_filter = ('slug',)
    empty_value_display = '-пусто-'


@admin.register(Comment)
class Comment(admin.ModelAdmin):
    list_display = (
        'pk',
        'author',
        'text',
        'post',
        'created',
    )
    list_editable = ('text',)
    search_fields = (
        'created',
        'author',
    )
    list_filter = ('created',)
    empty_value_display = '-пусто-'


@admin.register(Follow)
class Follow(admin.ModelAdmin):
    list_display = (
        'pk',
        'author',
        'user',
    )
    search_fields = (
        'user',
        'author',
    )
    list_filter = ('user',)
    empty_value_display = '-пусто-'
