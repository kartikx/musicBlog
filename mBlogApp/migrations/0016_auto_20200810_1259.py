# Generated by Django 3.0.8 on 2020-08-10 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mBlogApp', '0015_userprofile_changed_profile_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='changed_profile_photo',
            field=models.BooleanField(default=False),
        ),
    ]
