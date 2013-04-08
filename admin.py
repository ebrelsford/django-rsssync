from django.contrib import admin

from .models import RssEntry, RssFeed


class RssEntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'feed',)
    list_filter = ('feed',)
    search_fields = ('title',)


class RssFeedAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'is_active',)
    list_filter = ('is_active',)
    search_fields = ('name',)


admin.site.register(RssEntry, RssEntryAdmin)
admin.site.register(RssFeed, RssFeedAdmin)
