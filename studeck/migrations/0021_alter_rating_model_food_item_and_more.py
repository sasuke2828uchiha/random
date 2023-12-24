# Generated by Django 4.2.7 on 2023-12-24 11:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('studeck', '0020_alter_food_items_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating_model',
            name='food_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='studeck.food_items'),
        ),
        migrations.AlterField(
            model_name='rating_model',
            name='user_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='studeck.student_info'),
        ),
    ]
