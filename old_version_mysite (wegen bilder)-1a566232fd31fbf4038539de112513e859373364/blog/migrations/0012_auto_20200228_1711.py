# Generated by Django 2.1.2 on 2020-02-28 16:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_auto_20200228_1333'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='background_color',
        ),
        migrations.RemoveField(
            model_name='post',
            name='font_color',
        ),
    ]
