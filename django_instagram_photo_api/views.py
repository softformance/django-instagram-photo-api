import logging
import requests
from .app_settings import IG_URL, GET_MEDIAS_COUNT
from .models import InstagramApp, Tag, Post
from .utils import get_redirect_uri, sync_by_tag
from .exceptions import JsonException
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
# from django.core import serializers
from django.contrib.auth.decorators import login_required

IG_OAUTH_URL = '%s/oauth' % IG_URL

logger = logging.getLogger('default')


@login_required()
def access_token(request):
    code = request.GET['code']
    app_id = request.GET['app_id']
    app = InstagramApp.objects.get(id=app_id)

    data = {
        'client_id': app.client_id,
        'client_secret': app.secret_id,
        'grant_type': 'authorization_code',
        'redirect_uri': get_redirect_uri(request, app_id),
        'code': code
    }

    resp = requests.post(IG_OAUTH_URL + '/access_token', data=data)
    if resp.status_code == 200:
        resp = resp.json()
        app.access_token = resp['access_token']
        app.save()
        return redirect(reverse('admin:%s_%s_change' % (
            app._meta.app_label, app._meta.model_name), args=(app_id,)))
    else:
        return HttpResponse(resp)


@login_required()
def access_token_authorize(request, app_id=1):
    redirect_uri = get_redirect_uri(request, app_id)
    app = InstagramApp.objects.get(id=app_id)
    return redirect(IG_OAUTH_URL + '/authorize/?client_id=' + app.client_id +
                    '&redirect_uri=' + redirect_uri + '&response_type=code')


@login_required()
def sync_by_app(request, app_id=None):

    if not app_id:
        app_id = request.POST['app_id']
    if not app_id:
        return

    try:
        app = InstagramApp.objects.get(id=app_id)
        token = app.access_token
        count = GET_MEDIAS_COUNT
        is_show = app.tag_is_show
    except:
        message = "Try to sync udefined app"
        logger.exception(message)
        return JsonException(message)

    tags = Tag.objects.filter(application_id=app_id)
    for tag in tags:
        sync_by_tag(app_id, tag.name, token, count, is_show)

    return redirect(reverse('admin:%s_%s_changelist' % (
        app._meta.app_label, 'post')))


def get_posts(request, app_id):
    order_by_param = ('?', 'created_at')
    result_dict = {}
    result_dict['from_site'] = 'instagram'

    try:
        app = InstagramApp.objects.get(id=app_id)
    except:
        result_dict['photos'] = None
        return JsonResponse(result_dict)

    #count
    try:
        count = int(request.GET.get('count'))
    except:
        count = app.tag_count

    #order_by
    if request.GET.get('order_by') in order_by_param:
        order_by = request.GET.get('order_by')
    else:
        order_by = app.tag_sort_by

    params = {'application_id': app_id}
    tags = request.GET.getlist('tags')
    if tags:

        params['tags__name__in'] = tags

    posts = Post.objects.filter(**params)\
        .filter(show=True) \
        .order_by(order_by) \
        .distinct() \
        .values('media_id', 'photo', 'link', 'caption', 'photo_height', 
            'photo_width')[:count]

    
    result_dict['photos'] = list(posts)

    return JsonResponse(result_dict)
