# Generated by Django 2.1.3 on 2019-04-05 01:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='img_url',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]