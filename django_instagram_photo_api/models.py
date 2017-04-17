# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.db.models import signals

from easy_thumbnails.fields import ThumbnailerImageField
from django_celery_beat.models import PeriodicTask, PeriodicTasks, \
    IntervalSchedule, CrontabSchedule, SolarSchedule


class InstagramApp(models.Model):
    TYPE_OF_SORT = (
        ('created_at', 'DATE'),
        ('?', 'RANDOM'),
    )
    name = models.CharField(max_length=50, verbose_name=_('Application Name'))
    client_id = models.CharField(
        max_length=50, verbose_name=_('Instagram App Client ID'))
    secret_id = models.CharField(
        max_length=50, verbose_name=_('Instagram App Secret ID'))
    is_auto_access_token = models.BooleanField(
        verbose_name=_('Get access token automatically'), default=True)
    access_token = models.CharField(
        max_length=100, verbose_name=_('Access Token'),
        null=True, blank=True)
    tag_is_show = models.BooleanField(
        verbose_name=_('Show posts'), default=False)
    tag_sort_by = models.CharField(
        verbose_name=_('Type of sort'), choices=TYPE_OF_SORT, default='date', max_length=60)
    tag_count = models.PositiveSmallIntegerField(default=6)

    class Meta:
        verbose_name = _('Instagram Application')
        verbose_name_plural = _('Instagram Applications')

    def __str__(self):
        return '%s from application %s' % (self.id, self.name)


class TaskShedulerInstagram(PeriodicTask):
    periodic_task = models.ForeignKey(InstagramApp, on_delete=models.SET_NULL, 
        blank=True, null=True, related_name='periodic_task')


class Tag(models.Model):
    application = models.ForeignKey(
        InstagramApp, related_name='app_tag', default=1)
    name = models.CharField(max_length=50, verbose_name=_('Tag name'))

    class Meta:
        verbose_name = _('tag')
        verbose_name_plural = _('Tags')
        unique_together = (("application", "name"),) 

    def __str__(self):
        return '%s - application ID: %s' % (self.name, self.application)

    def save(self, *args, **kwargs):
        self.name = self.name.lower() 
        super(Tag, self).save(*args, **kwargs)


class Post(models.Model):
    application = models.ForeignKey(InstagramApp, related_name='app_post')
    media_id = models.CharField(_('Media ID'), max_length=100)
    photo = ThumbnailerImageField(upload_to='instagram_photos', height_field='photo_height', 
        width_field='photo_width')
    photo_height = models.PositiveIntegerField(default=0, editable=False)
    photo_width = models.PositiveIntegerField(default=0, editable=False)
    link = models.URLField(_('Link'))
    tags = models.ManyToManyField(Tag)
    caption = models.TextField(
        verbose_name=_('Caption text'),
        default='', blank=True, null=True)
    username = models.CharField(
        _('Instagram Username'), max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    show = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('post')
        verbose_name_plural = _('Posts')

        unique_together = (("application", "media_id"),)

    def get_thumb_url(self):
        try:
            return self.photo['thumb'].url
        except:
            return None


signals.pre_delete.connect(PeriodicTasks.changed, sender=TaskShedulerInstagram)
signals.pre_save.connect(PeriodicTasks.changed, sender=TaskShedulerInstagram)
signals.pre_delete.connect(
    PeriodicTasks.update_changed, sender=IntervalSchedule)
signals.post_save.connect(
    PeriodicTasks.update_changed, sender=IntervalSchedule)
signals.post_delete.connect(
    PeriodicTasks.update_changed, sender=CrontabSchedule)
signals.post_save.connect(
    PeriodicTasks.update_changed, sender=CrontabSchedule)
signals.post_delete.connect(
    PeriodicTasks.update_changed, sender=SolarSchedule)
signals.post_save.connect(
    PeriodicTasks.update_changed, sender=SolarSchedule)