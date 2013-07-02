import feedparser
import datetime

from .models import RssEntry


class RssSyncHelper(object):

    def __init__(self, feed):
        self.feed = feed

    def save_entry(self, result):
        pub_date = result.updated_parsed
        published = datetime.date(pub_date[0], pub_date[1], pub_date[2])
        return RssEntry.objects.get_or_create(
            title=result.title,
            feed=self.feed,
            summary=result.content[0]['value'],
            link=result.link,
            date=published,
        )

    def sync(self):
        feed = feedparser.parse(self.feed.url)
        for entry in feed.entries:
            self.save_entry(entry)

    def sync_wordpress_paginated(self, page):
        """Sync a Wordpress paginated feed"""
        feed = feedparser.parse('%s&paged=%d' % (self.feed.url, page))
        for entry in feed.entries:
            self.save_entry(entry)
