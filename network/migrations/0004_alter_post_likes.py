# Generated by Django 3.2.5 on 2021-07-31 02:39

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_alter_post_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(blank=True, default=0, related_name='lided_posts', to=settings.AUTH_USER_MODEL),
        ),
    ]
