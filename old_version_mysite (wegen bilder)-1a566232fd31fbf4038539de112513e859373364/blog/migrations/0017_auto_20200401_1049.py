# Generated by Django 2.1.2 on 2020-04-01 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0016_auto_20200401_1046'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='meta_description',
            field=models.CharField(blank=True, max_length=159),
        ),
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.CharField(blank=True, max_length=159),
        ),
        migrations.AlterField(
            model_name='section',
            name='description',
            field=models.CharField(blank=True, max_length=159),
        ),
        migrations.AlterField(
            model_name='type',
            name='description',
            field=models.CharField(blank=True, max_length=159),
        ),
    ]
