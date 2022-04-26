# Generated by Django 4.0.4 on 2022-04-26 03:21

import django.contrib.auth.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.IntegerField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('updated_by', models.IntegerField(blank=True, null=True)),
                ('username', models.CharField(max_length=255, unique=True, verbose_name='Usuario')),
                ('first_name', models.CharField(max_length=255, verbose_name='Nombre(s)')),
                ('last_name', models.CharField(max_length=255, verbose_name='Apellido(s)')),
                ('identification', models.CharField(blank=True, max_length=255, null=True, verbose_name='Identificación')),
                ('cellphone', models.CharField(max_length=255, verbose_name='Teléfono')),
                ('email', models.CharField(blank=True, db_index=True, max_length=255, null=True)),
                ('biography', models.TextField(verbose_name='Biografía')),
                ('photo', models.CharField(max_length=255, verbose_name='Foto')),
                ('rol', models.CharField(choices=[('admin', 'Administrador'), ('evaluator', 'Evaluador'), ('writer', 'Escritor')], max_length=9)),
                ('staff', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Usuario',
                'verbose_name_plural': 'Usuarios',
                'db_table': 'user',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
