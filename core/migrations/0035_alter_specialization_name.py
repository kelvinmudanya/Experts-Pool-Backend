# Generated by Django 3.2.4 on 2022-06-24 08:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0034_auto_20220624_0827'),
    ]

    operations = [
        migrations.AlterField(
            model_name='specialization',
            name='name',
            field=models.CharField(max_length=1000),
        ),
        
    ]
