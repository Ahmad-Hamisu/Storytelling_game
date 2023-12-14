from django.contrib import admin
from .models import Story, Tweet


class TweetInline(admin.TabularInline):
    model = Tweet
    extra = 1  # Number of empty forms to display


class StoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    inlines = [TweetInline]


class TweetAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'created_at', 'votes', 'story')
    list_filter = ('user', 'story')
    search_fields = ('user__username', 'content')


admin.site.register(Story, StoryAdmin)
admin.site.register(Tweet, TweetAdmin)
