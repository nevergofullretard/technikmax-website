# Generated by Django 2.1.2 on 2020-03-21 08:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_auto_20200320_2221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='next',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.Post'),
        ),
    ]