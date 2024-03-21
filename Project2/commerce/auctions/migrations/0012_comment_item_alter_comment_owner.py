# Generated by Django 4.0.1 on 2024-01-28 14:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_bid_bidlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='item',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='commentitems', to='auctions.listing'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comment',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commenters', to=settings.AUTH_USER_MODEL),
        ),
    ]
