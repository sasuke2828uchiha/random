# Generated by Django 4.2.7 on 2023-12-14 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studeck', '0014_checkpresence'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkpresence',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
