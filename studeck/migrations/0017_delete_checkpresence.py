# Generated by Django 4.2.7 on 2023-12-14 12:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('studeck', '0016_remove_checkpresence_date'),
    ]

    operations = [
        migrations.DeleteModel(
            name='checkpresence',
        ),
    ]
