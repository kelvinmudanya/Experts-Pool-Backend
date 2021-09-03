# Generated by Django 3.2.4 on 2021-09-03 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20210711_1616'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='application_status',
            field=models.CharField(choices=[('pending_approval', 'Pending Approval'), ('approved_by_partner_state', 'Approved By Partner State'), ('approval_complete', 'Approval Complete'), ('rejected', 'Rejected')], default='pending_approval', max_length=255),
        ),
    ]
