# Generated by Django 3.2.4 on 2022-03-06 15:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_profile_cv'),
    ]

    operations = [
        migrations.CreateModel(
            name='AcademicQualificationType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('degree_level', models.CharField(max_length=500)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OutbreakType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('label', models.CharField(max_length=500)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='outbreak',
            name='detailed_information',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='outbreak',
            name='eligibility_criteria',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='outbreak',
            name='general_information',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='outbreak',
            name='other_information',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='outbreak',
            name='requirements',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='references',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='ProfileAcademicQualification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('field_of_study', models.DateField()),
                ('institution', models.CharField(max_length=500)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.profile')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='outbreak',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.outbreaktype'),
        ),
    ]