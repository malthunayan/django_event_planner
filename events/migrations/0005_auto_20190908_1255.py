# Generated by Django 2.2.5 on 2019-09-08 12:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0004_auto_20190908_1241'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='maximum_number_of_tickets',
        ),
        migrations.RemoveField(
            model_name='event',
            name='tickets',
        ),
        migrations.AddField(
            model_name='event',
            name='tickets_available',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.CreateModel(
            name='BookTicket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tickets', models.PositiveIntegerField()),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.Event')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]