# Generated by Django 3.2.4 on 2022-06-23 07:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0028_auto_20220623_0958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='region',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]
