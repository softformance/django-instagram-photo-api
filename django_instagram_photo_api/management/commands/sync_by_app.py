from django.core.management.base import BaseCommand, CommandError
from django_instagram_photo_api.models import InstagramApp, Tag, Post
from django_instagram_photo_api.utils import sync_by_tag, save_post, get_medias_by_tag

class Command(BaseCommand):
    help = 'Sync your app with hashtags by added list of id.'

    def add_arguments(self, parser):
        parser.add_argument('application_id', nargs='+', type=int)

    def handle(self, *args, **options):
        for app_id in options['application_id']:
            try:
                app = InstagramApp.objects.get(pk=app_id)
            except InstagramApp.DoesNotExist:
                raise CommandError('Application "%s" does not exist' % app_id)

            is_show = app.tag_is_show
            count = app.tag_count
            token = app.access_token

            tags = Tag.objects.filter(application_id=app_id)
            for tag in tags:
                sync_by_tag(app_id, tag.name, token, count, is_show)