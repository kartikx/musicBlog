# Generated by Django 3.0.8 on 2020-07-30 10:49

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mBlogApp', '0010_post_upvotes'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='upvotedby',
            field=models.ManyToManyField(blank=True, related_name='liked_posts', to=settings.AUTH_USER_MODEL),
        ),
    ]