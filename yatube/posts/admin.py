from django.contrib import admin

from .models import Comment, Group, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'text',
        'pub_date',
        'author',
        'group',
    )
    list_editable = ('group',)
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'slug',
        'description',
    )
    list_editable = ('title', 'slug')
    list_display_links = None
    list_filter = ('title',)
    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'text',
        'created',
        'author',
    )
    search_fields = ('text',)
    list_filter = ('author',)
    empty_value_display = '-пусто-'
