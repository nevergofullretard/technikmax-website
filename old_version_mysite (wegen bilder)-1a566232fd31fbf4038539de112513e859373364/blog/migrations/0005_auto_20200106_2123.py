# Generated by Django 2.1.2 on 2020-01-06 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20200106_2009'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='font_color',
            field=models.CharField(default='black', max_length=100),
        ),
        migrations.AddField(
            model_name='project',
            name='font_color',
            field=models.CharField(default='black', max_length=100),
        ),
    ]