# Generated by Django 3.2.12 on 2022-04-08 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20220402_2048'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='meta_data',
            field=models.TextField(blank=True, null=True, verbose_name='Meta Data'),
        ),
    ]
