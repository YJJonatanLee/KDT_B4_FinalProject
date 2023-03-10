# Generated by Django 4.0.3 on 2023-01-11 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Photos',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('origin_photo', models.ImageField(null=True, upload_to='origin')),
                ('converte_photo', models.ImageField(upload_to='converte')),
                ('background_color', models.CharField(default='', max_length=3)),
                ('background_photo', models.ImageField(upload_to='background')),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('origin_photo', models.ImageField(null=True, upload_to='orgin')),
            ],
        ),
    ]
