# Generated by Django 5.1.6 on 2025-02-28 11:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kuzov', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='zakaznaryad',
            name='predoplata',
        ),
        migrations.CreateModel(
            name='Oplata',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=0)),
                ('time_create', models.DateTimeField(auto_now_add=True, null=True)),
                ('zakaz', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='oplata', to='kuzov.zakaznaryad')),
            ],
        ),
    ]
