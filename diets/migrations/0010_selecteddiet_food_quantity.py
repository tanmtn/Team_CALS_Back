# Generated by Django 4.2.5 on 2023-10-05 05:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("diets", "0009_alter_selecteddiet_food_calorie"),
    ]

    operations = [
        migrations.AddField(
            model_name="selecteddiet",
            name="food_quantity",
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]
