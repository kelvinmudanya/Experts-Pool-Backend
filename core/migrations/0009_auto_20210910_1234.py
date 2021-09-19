# Generated by Django 3.2.4 on 2021-09-10 09:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_profile_application_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='profiledeployment',
            name='region',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.region'),
        ),
        migrations.AddField(
            model_name='profiledeployment',
            name='status',
            field=models.CharField(choices=[('initiated', 'Initiated'), ('ended', 'Ended')], default='initiated', max_length=100),
        ),
        migrations.AddField(
            model_name='user',
            name='attached_region',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.region'),
        ),
        migrations.AddField(
            model_name='user',
            name='level',
            field=models.CharField(choices=[('regional', 'Regional'), ('eac', 'EAC'), ('rde', 'RDE')], default='rde', max_length=50),
        ),
        migrations.AlterField(
            model_name='profiledeployment',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deployments', to='core.profile'),
        ),
    ]
