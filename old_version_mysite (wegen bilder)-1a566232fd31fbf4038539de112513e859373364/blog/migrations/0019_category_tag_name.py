# Generated by Django 2.1.2 on 2020-04-01 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0018_auto_20200401_1053'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='tag_name',
            field=models.CharField(blank=True, max_length=110),
        ),
    ]