# Generated by Django 3.2.6 on 2021-08-20 07:42

import cvat_adas_demo.dataset_repo.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('engine', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='GitData',
            fields=[
                ('task', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='engine.task')),
                ('url', models.URLField(max_length=2000)),
                ('path', models.CharField(max_length=256)),
                ('sync_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(default=cvat_adas_demo.dataset_repo.models.GitStatusChoice['NON_SYNCED'], max_length=20)),
                ('lfs', models.BooleanField(default=True)),
            ],
        ),
    ]
