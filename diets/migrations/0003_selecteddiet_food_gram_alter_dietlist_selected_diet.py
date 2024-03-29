# Generated by Django 4.2.5 on 2023-10-03 09:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("diets", "0002_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="selecteddiet",
            name="food_gram",
            field=models.PositiveIntegerField(default=150),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="dietlist",
            name="selected_diet",
            field=models.ManyToManyField(related_name="diets", to="diets.selecteddiet"),
        ),
    ]
