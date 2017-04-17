from __future__ import absolute_import, unicode_literals

from django_instagram_photo_api.models import InstagramApp, Tag, Post
from django_instagram_photo_api.utils import sync_by_tag, save_post, get_medias_by_tag

from celery import shared_task

@shared_task(name='Sync Instagram application by id')
def sync_tag_by_app_id(*args):
    for app_id in args:
        try:
            app = InstagramApp.objects.get(pk=app_id)
        except InstagramApp.DoesNotExist:
            print('DOESNOT EXIST')
            continue

        is_show = app.tag_is_show
        count = app.tag_count
        token = app.access_token


        tags = Tag.objects.filter(application_id=app_id)
        for tag in tags:
            sync_by_tag(app_id, tag.name, token, count, is_show)