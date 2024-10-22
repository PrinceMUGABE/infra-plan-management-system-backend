# Generated by Django 5.0.7 on 2024-10-13 11:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('plannerApp', '0004_alter_planner_created_by_alter_planner_no_experience'),
        ('projectApp', '0003_rename_name_project_field_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlannedProject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending', max_length=10)),
                ('duration', models.IntegerField(help_text='Duration in days')),
                ('planned_date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('planned_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='planned_projects', to='plannerApp.planner')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='planned_projects', to='projectApp.project')),
            ],
            options={
                'unique_together': {('project', 'planned_by')},
            },
        ),
    ]
