# Generated by Django 2.1.2 on 2020-04-01 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0020_auto_20200401_1057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='tag_name',
            field=models.CharField(blank=True, max_length=35, unique=True),
        ),
    ]
