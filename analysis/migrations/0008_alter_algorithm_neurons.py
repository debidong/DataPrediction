# Generated by Django 4.2.7 on 2023-12-11 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0007_result_model'),
    ]

    operations = [
        migrations.AlterField(
            model_name='algorithm',
            name='neurons',
            field=models.CharField(max_length=256),
        ),
    ]
