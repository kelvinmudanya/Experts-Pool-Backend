# Generated by Django 3.2.4 on 2021-09-19 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20210910_1234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='outbreak',
            name='competencies',
            field=models.ManyToManyField(blank=True, related_name='outbreaks', to='core.Competence'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='competencies',
            field=models.ManyToManyField(to='core.Competence'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='middle_name',
            field=models.CharField(blank=True, default=1, max_length=30),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='profile',
            name='note',
            field=models.TextField(blank=True, default='_'),
            preserve_default=False,
        ),
    ]
