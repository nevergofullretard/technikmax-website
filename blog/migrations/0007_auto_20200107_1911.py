# Generated by Django 2.1.2 on 2020-01-07 18:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20200106_2134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='background_color',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='background_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=True, to='blog.Images'),
        ),
        migrations.AlterField(
            model_name='project',
            name='background_color',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='background_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.Images'),
        ),
    ]
