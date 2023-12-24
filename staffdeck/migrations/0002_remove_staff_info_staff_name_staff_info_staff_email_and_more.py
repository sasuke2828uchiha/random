# Generated by Django 4.2.7 on 2023-11-17 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staffdeck', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='staff_info',
            name='staff_name',
        ),
        migrations.AddField(
            model_name='staff_info',
            name='staff_email',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='staff_info',
            name='staff_fname',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AddField(
            model_name='staff_info',
            name='staff_id',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AddField(
            model_name='staff_info',
            name='staff_lname',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='staff_info',
            name='staff_mess',
            field=models.CharField(default='', max_length=10),
        ),
    ]
