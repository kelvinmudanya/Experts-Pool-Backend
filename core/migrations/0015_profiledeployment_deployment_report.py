# Generated by Django 3.2.4 on 2022-03-16 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_profiledeployment_accepted_by_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='profiledeployment',
            name='deployment_report',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
