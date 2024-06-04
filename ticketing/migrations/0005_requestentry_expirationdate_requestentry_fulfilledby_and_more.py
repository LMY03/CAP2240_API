# Generated by Django 5.0.6 on 2024-05-29 16:53

import datetime
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0004_alter_requestentry_status_alter_requestentry_storage'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='requestentry',
            name='expirationDate',
            field=models.DateField(default=datetime.date(2024, 8, 28)),
        ),
        migrations.AddField(
            model_name='requestentry',
            name='fulfilledBy',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fulfilled_entries', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='requestentry',
            name='isExpired',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='requestentry',
            name='requestDate',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='requestentry',
            name='requester',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='requested_entries', to=settings.AUTH_USER_MODEL),
        ),
    ]
