# Generated by Django 4.0.1 on 2024-01-26 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_alter_listing_owner_watchlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='firstbid',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=16),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='bid',
            name='bid',
            field=models.DecimalField(decimal_places=2, max_digits=16),
        ),
    ]
