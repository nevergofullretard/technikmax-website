# Generated by Django 2.1.2 on 2020-04-01 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0022_auto_20200401_1059'),
    ]

    operations = [
        migrations.CreateModel(
            name='Texte',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField(blank=True)),
            ],
        ),
    ]
