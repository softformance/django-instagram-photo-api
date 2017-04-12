import os
import logging
import requests
from django.core.mail import mail_admins

from django.core.files.base import ContentFile
from .models import Post, Tag
from .exceptions import JsonException
from datetime import datetime
from .app_settings import IG_URL, GET_MEDIAS_COUNT

REDIRECT_URI_SUFIX = 'instagram_app/access_token/token'

logger = logging.getLogger('default')



def invalid_token_handler():
    message = "Your token has expired or invalid."
    mail_admins('Instagram Application', message, fail_silently=True)


def get_redirect_uri(request, app_id):
    host = request.get_host()
    prefix = 'https' if request.is_secure() else 'http'
    return '%s://%s/%s?app_id=%s' % (prefix, host, REDIRECT_URI_SUFIX, app_id)


def get_medias_by_tag(tag, access_token, count):
    url = '%s/v1/tags/%s/media/recent?access_token=%s&count=%s' % (
        IG_URL, tag, access_token, count)
    try:
        resp = requests.get(url)
        if resp.status_code == 200:
            return resp.json()
        else:
            if resp.status_code == 400:
                invalid_token_handler()
            resp = resp.json()
            message = resp['meta'].get('error_message')
            logger.exception(message)
            raise Exception(message)
    except Exception as e:
        message = "Error while fetching medias_by_tag: %s" % e
        logger.exception(message)
        raise JsonException(message)


def get_media_by_code(code, access_token):
    url = '%s/v1/media/shortcode/%s?access_token=%s' % (
        IG_URL, code, access_token)
    try:
        resp = requests.get(url)
        if resp.status_code == 200:
            return None, resp.json().get('data')
        elif resp.status_code == 404:
            return resp.reason, None
        else:
            if resp.status_code == 400:
                invalid_token_handler()
            return resp.json()['meta'].get('error_message'), None
    except:
        logger.exception("Error while fetching medias_by_tag")
        return 'Error while fetching medias_by_tag', None


def save_post(app_id, media, is_show):

    media_id = media['id']
    link = media['link']
    caption = media['caption']['text']
    media_url = media['images']['standard_resolution']['url']
    created_at = datetime.fromtimestamp(int(media['created_time']))
    username = media['user']['username']

    post, created = Post.objects.get_or_create(
        media_id=media_id, application_id=app_id,
        defaults={
            'link': link,
            'username': username,
            'caption': caption,
            'created_at': created_at,
            'show': is_show
        }
    )

    if created:
        # save image
        photo_content = ContentFile(requests.get(media_url).content)
        post.photo.save(os.path.basename(media_url), photo_content)
        # save tags
        app_tags = Tag.objects.filter(application_id=app_id)
        tags = [tag for tag in app_tags if tag.name in media['tags']]
        for tag in tags:
            post.tags.add(tag)
        if tags:
            post.save()
    return post


def get_media_by_url(application, url):
    code = url.split('/')[4]
    return get_media_by_code(code, application.access_token)


def sync_by_tag(app_id, tag, token, count, is_show):
    medias = get_medias_by_tag(tag, token, count)
    if medias and medias.get('data'):
        for media in medias['data']:
            if media['type'] == 'image':
                save_post(app_id, media, is_show)
