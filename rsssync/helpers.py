import feedparser
import datetime
from pyquery import PyQuery as pq

from .models import RssEntry


def add_custom_acceptable_elements(elements):
    """
    Add custom acceptable elements so iframes and other potential video
    elements will get synched.
    """
    elements += list(feedparser._HTMLSanitizer.acceptable_elements)
    feedparser._HTMLSanitizer.acceptable_elements = set(elements)

custom_acceptable_elements = ['iframe', 'embed', 'object',]
add_custom_acceptable_elements(custom_acceptable_elements)


class RssSyncHelper(object):

    def __init__(self, feed):
        self.feed = feed

    def save_entry(self, result):
        content = result.content[0]['value']
        pub_date = result.updated_parsed
        published = datetime.date(pub_date[0], pub_date[1], pub_date[2])
        return RssEntry.objects.get_or_create(
            title=result.title,
            feed=self.feed,
            summary=content,
            link=result.link,
            date=published,
            cover_image_url=self.get_cover_image(content),
        )

    def get_cover_image(self, content):
        """
        Try to find a cover image for the entry--just the first image in the
        content.
        """
        try:
            d = pq(content)
            return d('img')[0].attrib['src']
        except Exception:
            return None

    def sync(self):
        feed = feedparser.parse(self.feed.url)
        for entry in feed.entries:
            self.save_entry(entry)

    def sync_wordpress_paginated(self, page):
        """Sync a Wordpress paginated feed"""
        feed = feedparser.parse('%s&paged=%d' % (self.feed.url, page))
        for entry in feed.entries:
            self.save_entry(entry)
