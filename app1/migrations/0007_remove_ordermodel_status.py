# Generated by Django 3.2.3 on 2021-05-29 11:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0006_ordermodel_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ordermodel',
            name='status',
        ),
    ]
