# Generated by Django 4.0.4 on 2022-06-30 02:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_score_extra'),
    ]

    operations = [
        migrations.AlterField(
            model_name='score',
            name='extra',
            field=models.CharField(blank=True, choices=[('general', 'Descripción general'), ('files', 'Archivos')], default='', max_length=10, null=True),
        ),
    ]
