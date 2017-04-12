# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-12 14:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import easy_thumbnails.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='InstagramApp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Application Name')),
                ('client_id', models.CharField(max_length=50, verbose_name='Instagram App Client ID')),
                ('secret_id', models.CharField(max_length=50, verbose_name='Instagram App Secret ID')),
                ('is_auto_access_token', models.BooleanField(default=True, verbose_name='Get access token automatically')),
                ('access_token', models.CharField(blank=True, max_length=100, null=True, verbose_name='Access Token')),
                ('tag_is_show', models.BooleanField(default=False, verbose_name='Show posts')),
                ('tag_sort_by', models.CharField(choices=[('created_at', 'DATE'), ('?', 'RANDOM')], default='date', max_length=60, verbose_name='Type of sort')),
                ('tag_count', models.PositiveSmallIntegerField(default=6)),
            ],
            options={
                'verbose_name_plural': 'Instagram Applications',
                'verbose_name': 'Instagram Application',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('media_id', models.CharField(max_length=100, verbose_name='Media ID')),
                ('photo', easy_thumbnails.fields.ThumbnailerImageField(height_field='photo_height', upload_to='instagram_photos', width_field='photo_width')),
                ('photo_height', models.PositiveIntegerField(default=0, editable=False)),
                ('photo_width', models.PositiveIntegerField(default=0, editable=False)),
                ('link', models.URLField(verbose_name='Link')),
                ('caption', models.TextField(blank=True, default='', null=True, verbose_name='Caption text')),
                ('username', models.CharField(blank=True, max_length=100, null=True, verbose_name='Instagram Username')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('show', models.BooleanField(default=False)),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='app_post', to='django_instagram_photo_api.InstagramApp')),
            ],
            options={
                'verbose_name_plural': 'Posts',
                'verbose_name': 'post',
            },
        ),
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Tag name')),
                ('application', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='app_tag', to='django_instagram_photo_api.InstagramApp')),
            ],
            options={
                'verbose_name_plural': 'Tags',
                'verbose_name': 'tag',
            },
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(to='django_instagram_photo_api.Tag'),
        ),
        migrations.AlterUniqueTogether(
            name='tag',
            unique_together=set([('application', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='post',
            unique_together=set([('application', 'media_id')]),
        ),
    ]
