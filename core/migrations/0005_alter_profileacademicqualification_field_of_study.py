# Generated by Django 3.2.4 on 2022-03-06 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20220306_1811'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profileacademicqualification',
            name='field_of_study',
            field=models.CharField(max_length=500),
        ),
    ]
