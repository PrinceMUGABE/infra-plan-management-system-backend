# Generated by Django 5.0.7 on 2024-10-01 08:11

import django.core.validators
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=30, unique=True, validators=[django.core.validators.EmailValidator(message='Invalid email format'), django.core.validators.RegexValidator(message='Email must be a Gmail address', regex='^[\\w\\.-]+@gmail\\.com$')])),
                ('username', models.CharField(max_length=50, unique=True)),
                ('phone', models.CharField(max_length=10, unique=True, validators=[django.core.validators.RegexValidator(message='Phone number must start with 078, 079, 073, or 072 and be 10 digits long', regex='^(078|079|073|072)\\d{7}$')])),
                ('role', models.CharField(choices=[('admin', 'Admin'), ('planner', 'Planner'), ('engineer', 'Engineer'), ('stakeholder', 'Stakeholder')], max_length=20)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
