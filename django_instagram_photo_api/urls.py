# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^access_token/authorize/(?P<app_id>\d+)?$', views.access_token_authorize, name='access-token-authorize'),
    # url(r'^access_token/code', views.access_token_code),
    url(r'^access_token/token', views.access_token),
    url(r'^sync_by_app/(?P<app_id>\d+)?$', views.sync_by_app, name='sync-by-app'),
    url(r'^sync_by_app', views.sync_by_app, name='sync-by-app'),
    url(r'^get_posts/(?P<app_id>\d+)?$', views.get_posts, name='get-posts'),
]
