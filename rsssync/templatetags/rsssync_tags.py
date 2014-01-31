from django import template

from classytags.arguments import Argument
from classytags.core import Options
from classytags.helpers import AsTag

from rsssync.models import RssFeed

register = template.Library()


class GetLatestEntries(AsTag):
    options = Options(
        'for',
        Argument('feed', required=True, resolve=True),
        Argument('limit', required=False, resolve=True),
        'as',
        Argument('varname', required=True, resolve=False),
    )

    def get_value(self, context, feed, limit=5):
        if not isinstance(feed, RssFeed):
            try:
                feed = RssFeed.objects.get(name=feed)
            except RssFeed.DoesNotExist:
                raise
        return feed.rssentry_set.all().order_by('-date')[:limit]

register.tag(GetLatestEntries)
