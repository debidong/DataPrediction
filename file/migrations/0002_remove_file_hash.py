# Generated by Django 4.2.7 on 2023-11-16 13:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('file', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='hash',
        ),
    ]