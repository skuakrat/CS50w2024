# Generated by Django 4.0.1 on 2024-01-27 17:45

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_remove_watchlist_user_watchlist_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='watch',
            field=models.ManyToManyField(blank=True, related_name='watchers', to=settings.AUTH_USER_MODEL),
        ),
    ]