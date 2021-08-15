# Generated by Django 3.2.5 on 2021-08-01 23:02

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_alter_post_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='followers',
            field=models.ManyToManyField(blank=True, related_name='_network_user_followers_+', to=settings.AUTH_USER_MODEL),
        ),
    ]