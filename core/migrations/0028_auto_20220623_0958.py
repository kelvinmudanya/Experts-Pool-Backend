# Generated by Django 3.2.4 on 2022-06-23 06:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0027_profile_other_occupation'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='managerial_experience',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='region',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.CreateModel(
            name='Specialization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('occupation',
                 models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.occupation')),
            ],
            options={
                'verbose_name': 'Specialization',
                'verbose_name_plural': 'Specializations',
            },
        ),
        migrations.AddField(
            model_name='competence',
            name='specialization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                    to='core.specialization'),
        ),
    ]
