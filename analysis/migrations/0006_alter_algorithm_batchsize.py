# Generated by Django 4.2.7 on 2023-11-24 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0005_algorithm_selected'),
    ]

    operations = [
        migrations.AlterField(
            model_name='algorithm',
            name='batchSize',
            field=models.IntegerField(),
        ),
    ]