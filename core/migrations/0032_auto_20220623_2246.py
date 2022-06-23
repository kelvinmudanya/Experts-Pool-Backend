# Generated by Django 3.2.4 on 2022-06-23 19:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0031_detailedexperience_occupation'),
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='detailedexperience',
            name='no_of_people_managed',
            field=models.CharField(blank=True, choices=[('1-4', '1 To 4 People'), ('5-10', '5 To 10 People'),
                                                        ('10-20', '10 To 20 Years'), ('over-20', 'Over 20 Years')],
                                   max_length=255, null=True),
        ),
        migrations.CreateModel(
            name='ProfileLanguage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('proficiency_level', models.CharField(
                    choices=[('beginner', 'beginner'), ('intermediate', 'intermediate'), ('fluent', 'fluent'),
                             ('native_speaker', 'Native Speaker')], max_length=255)),
                ('language', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                               to='core.language')),
                ('profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                              to='core.profile')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
