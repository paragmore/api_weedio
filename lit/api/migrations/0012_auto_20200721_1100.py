# Generated by Django 3.0.8 on 2020-07-21 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_browser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='browser',
            name='timestamp',
            field=models.TimeField(auto_now_add=True),
        ),
    ]
