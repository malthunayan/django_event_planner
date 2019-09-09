# Generated by Django 2.2.5 on 2019-09-08 22:53

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_auto_20190908_1255'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='occurance',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='event',
            name='tickets_available',
            field=models.PositiveIntegerField(),
        ),
    ]
