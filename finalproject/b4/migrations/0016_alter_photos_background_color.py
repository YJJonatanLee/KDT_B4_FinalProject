# Generated by Django 4.1.5 on 2023-01-16 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("b4", "0015_merge_0011_merge_20230112_1749_0014_cameraimage"),
    ]

    operations = [
        migrations.AlterField(
            model_name="photos",
            name="background_color",
            field=models.CharField(default="0", max_length=3),
        ),
    ]
