# Generated by Django 3.0.6 on 2020-05-18 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='created_time',
            field=models.DateField(auto_now_add=True),
        ),
    ]
