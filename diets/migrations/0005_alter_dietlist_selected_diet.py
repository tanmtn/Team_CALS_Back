# Generated by Django 4.2.5 on 2023-10-03 14:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("diets", "0004_alter_dietlist_selected_diet"),
    ]

    operations = [
        migrations.AlterField(
            model_name="dietlist",
            name="selected_diet",
            field=models.ManyToManyField(
                blank=True, null=True, related_name="diets", to="diets.selecteddiet"
            ),
        ),
    ]
