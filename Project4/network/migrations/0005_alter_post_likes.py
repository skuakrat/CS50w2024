# Generated by Django 4.0.1 on 2024-02-03 17:43

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_alter_post_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(blank=True, null=True, related_name='posts_liked', to=settings.AUTH_USER_MODEL),
        ),
    ]
