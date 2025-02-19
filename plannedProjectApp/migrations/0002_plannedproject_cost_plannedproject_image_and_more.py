# Generated by Django 5.0.7 on 2024-10-13 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plannedProjectApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='plannedproject',
            name='cost',
            field=models.DecimalField(decimal_places=2, default=0, help_text='Cost of the project plan', max_digits=10),
        ),
        migrations.AddField(
            model_name='plannedproject',
            name='image',
            field=models.BinaryField(blank=True, help_text='Image of the project plan', null=True),
        ),
        migrations.AddField(
            model_name='plannedproject',
            name='location',
            field=models.CharField(default='', help_text='Location of the project plan', max_length=255),
        ),
    ]
