# Generated by Django 4.0.1 on 2024-01-27 18:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_alter_listing_watch'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Watchlist',
        ),
    ]
