from django.db import models
from django.utils.translation import ugettext_lazy as _


class RssFeed(models.Model):
    name = models.CharField(_('name'), max_length=256)
    url = models.URLField(_('url'))

    is_active = models.BooleanField(
        _('Active?'),
        default=True,
        help_text=_('Mark this feed enabled for syncing?'),
    )

    def __unicode__(self):
        return self.name


class RssEntry(models.Model):
    title = models.CharField(_('title'), max_length=500)
    summary = models.TextField(_('summary'), blank=True, null=True)
    link = models.URLField(_('link'), blank=True, null=True)
    date = models.DateTimeField(_('date'), blank=True, null=True)
    feed = models.ForeignKey('RssFeed')

    def __unicode__(self):
        return '%s: "%s"' % (self.feed.name, self.title)

    class Meta:
        verbose_name_plural = _('Rss entries')
