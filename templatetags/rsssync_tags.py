from django import template

from rsssync.models import RssFeed

register = template.Library()


class LatestEntries(template.Node):
    def __init__(self, feed, limit, varname):
        self.feed = feed
        self.limit = limit
        self.varname = varname

    def render(self, context):
        def resolve_or_not(var, context):
            if callable(getattr(var, 'resolve', None)):
                return var.resolve(context)
            return var

        feed = resolve_or_not(self.feed, context)
        limit = resolve_or_not(self.limit, context)
        varname = resolve_or_not(self.varname, context)

        if not isinstance(feed, RssFeed):
            try:
                feed = RssFeed.objects.get(name=feed)
            except RssFeed.DoesNotExist:
                raise

        context[varname] = feed.rssentry_set.all()[:int(limit)]
        return u''


@register.tag
def get_latest_entries(parser, token):
    ''' Returns the latest entries stored in the db.

        Run like so:

        {% get_latest_entries feed 5 as entries %}

        Will return the last 5 entries and store in the
        template context as "entries".
    '''
    bits = token.split_contents()
    if len(bits) < 4:
        raise template.TemplateSyntaxError(
            '"%s" tag takes at least 3 arguments' % bits[0]
        )

    limit = None
    try:
        _tag, feed, limit, _as, varname = bits
    except ValueError:
        _tag, feed, _as, varname = bits

    if limit is None:
        limit = 5

    try:
        # needed because it may not be passed via the
        # template token.
        limit = parser.compile_filter(limit)
    except TypeError:
        pass

    return LatestEntries(
        parser.compile_filter(feed),
        limit,
        parser.compile_filter(varname),
    )
