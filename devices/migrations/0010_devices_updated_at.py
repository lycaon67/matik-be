# Generated by Django 3.2 on 2024-03-24 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0009_channels_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='devices',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]