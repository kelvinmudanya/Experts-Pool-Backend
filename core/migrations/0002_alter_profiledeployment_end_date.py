# Generated by Django 3.2.4 on 2021-09-22 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profiledeployment',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
