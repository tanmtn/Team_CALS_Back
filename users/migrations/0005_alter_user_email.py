# Generated by Django 4.2.5 on 2023-09-25 02:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0004_alter_user_email_alter_user_username"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(max_length=200, unique=True),
        ),
    ]
