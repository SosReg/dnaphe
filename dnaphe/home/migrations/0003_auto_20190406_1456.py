# Generated by Django 2.1.3 on 2019-04-06 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_post_img_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='downvote',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='upvote',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
