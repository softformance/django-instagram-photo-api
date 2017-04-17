import os
import requests

from django import forms
from datetime import datetime
from django.urls import reverse
from django.contrib import admin
from django.conf.urls import url
from django.core.files.base import ContentFile
from django.forms.models import ModelForm

from .utils import get_media_by_url
from .models import Post, Tag, InstagramApp, TaskShedulerInstagram
from django_celery_beat.models import PeriodicTask
from django_celery_beat.admin import PeriodicTaskForm


class PostUrlForm(forms.ModelForm):
    url = forms.URLField(label='Insert link to photo', required=True)

    class Meta:
        model = Post
        fields = ['application', 'url']

    def clean(self):
        cleaned_data = super(PostUrlForm, self).clean()
        error, data = get_media_by_url(
            cleaned_data['application'], cleaned_data['url'])

        if error:
            raise forms.ValidationError(error)
        if data:
            cleaned_data.update(data)

        return cleaned_data


class PostAdmin(admin.ModelAdmin):

    change_list_template = 'django_instagram_photo_api/admin/post_change_list.html'

    list_display = ('application', 'thumb_image', 'get_username', 'caption',
                    'get_tags', 'created_at', 'show',)
    list_display_links = ('caption', )
    list_filter = ('application', 'tags', 'created_at', )
    list_editable = ('show', )
    search_fields = ['caption', 'tags__name']

    def save_model(self, request, obj, form, change):
        if request.POST.get('url'):
            data = form.cleaned_data
            obj.media_id = data['id']
            obj.link = data['link']
            obj.caption = data['caption']['text']
            media_url = data['images']['standard_resolution']['url']
            obj.created_at = datetime.fromtimestamp(
                int(data['created_time']))
            obj.username = data['user']['username']

            # save image
            photo_content = ContentFile(requests.get(media_url).content)
            obj.photo.save(os.path.basename(media_url), photo_content)
            # save tags
            app_tags = Tag.objects.filter(application_id=obj.application.id)
            tags = [tag for tag in app_tags if tag.name in data['tags']]
            for tag in tags:
                obj.tags.add(tag)
            if tags:
                obj.save()
            return

        obj.save()

    def get_apps(self):
        return InstagramApp.objects.all()

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['apps'] = self.get_apps()
        return super(PostAdmin, self).changelist_view(
            request, extra_context=extra_context)

    def get_tags(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])

    def thumb_image(self, obj):
        return '<a href="%s" target="_blank"><img src="%s"/></a>' % (
            obj.link, obj.get_thumb_url())

    def get_username(self, obj):
        if obj.username:
            return '<a href="https://www.instagram.com/%s" target="_blank">@%s</a>' % (
                obj.username, obj.username)

    def get_urls(self):
        urls = super(PostAdmin, self).get_urls()
        c_urls = [
            url(r'^add_by_url/$', self.add_by_url),
        ]
        return c_urls + urls

    def add_by_url(self, request):
        return self.add_view(request, form=PostUrlForm)

    def add_view(self, request, form=ModelForm, form_url='',
                 extra_context=None):
        self.form = form
        return super(PostAdmin, self).add_view(request, form_url, extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.form = ModelForm
        return super(PostAdmin, self).change_view(request, object_id, form_url,
                                                  extra_context)

    thumb_image.allow_tags = True
    get_username.allow_tags = True


class TagAdmin(admin.ModelAdmin):

    list_display = ('application', 'name',)
    list_filter = ('application', 'name', )


class TaskShedulerInline(admin.StackedInline):
    form = PeriodicTaskForm
    model = TaskShedulerInstagram
    max_num = 1
    classes = ['collapse']    

    fieldsets = (
        (None, {
            'fields': ('name', 'regtask', 'task', 'enabled'),
            'classes': ('extrapretty', 'wide'),
        }),
        ('Schedule', {
            'fields': ('interval', 'crontab'),
            'classes': ('extrapretty', 'wide'),
        }),
        ('Arguments', {
            'fields': ('args', 'kwargs'),
            'classes': ('extrapretty', 'wide'),
        }),
        ('Execution Options', {
            'fields': ('expires', 'queue', 'exchange', 'routing_key'),
            'classes': ('extrapretty', 'wide'),
        }),
    )


class InstagramAppAdmin(admin.ModelAdmin):

    list_display = ('id', 'name')

    inlines = [
        TaskShedulerInline,
    ]

    def response_change(self, request, obj):
        response = super(InstagramAppAdmin, self).response_change(request, obj)

        if obj.is_auto_access_token:
            post_url = reverse('access-token-authorize',
                               kwargs={'app_id': obj.id})
            response['location'] = post_url

        return response


admin.site.register(Post, PostAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(InstagramApp, InstagramAppAdmin)
