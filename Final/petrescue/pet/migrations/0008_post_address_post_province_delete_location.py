# Generated by Django 4.0.1 on 2024-02-15 18:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pet', '0007_remove_post_body_alter_post_breed'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='address',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='post',
            name='province',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='provinces', to='pet.province'),
        ),
        migrations.DeleteModel(
            name='Location',
        ),
    ]
