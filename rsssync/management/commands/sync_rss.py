from django.core.management.base import NoArgsCommand

from ...helpers import RssSyncHelper
from ...models import RssFeed


class Command(NoArgsCommand):
    help = 'Sync all RSS feeds.'

    def handle_noargs(self, **options):
        for feed in RssFeed.objects.filter(is_active=True):
            RssSyncHelper(feed).sync()
