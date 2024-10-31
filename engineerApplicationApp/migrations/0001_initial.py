# Generated by Django 5.0.7 on 2024-10-31 08:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('engineerApp', '0003_alter_engineer_created_by'),
        ('funded_project_app', '0002_alter_fundedproject_created_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='EngineerApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='engineerApp.engineer')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='funded_project_app.fundedproject')),
            ],
            options={
                'unique_together': {('created_by', 'project')},
            },
        ),
    ]
