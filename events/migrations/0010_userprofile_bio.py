# Generated by Django 2.2.5 on 2019-09-11 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0009_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='bio',
            field=models.CharField(default='', max_length=270, null=True),
        ),
    ]
