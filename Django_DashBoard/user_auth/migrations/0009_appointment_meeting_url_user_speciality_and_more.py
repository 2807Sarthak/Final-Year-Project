# Generated by Django 5.0.6 on 2024-06-13 18:01

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0008_alter_appointment_patient_desc'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='meeting_url',
            field=models.URLField(blank=True, default=None, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='speciality',
            field=models.CharField(blank=True, choices=[('Neuro', 'Neuro'), ('Cardio', 'Cardio'), ('Pediatrics', 'Pediatrics')], default=None, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='chosen_date',
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='chosen_time',
            field=models.TimeField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='doctor',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='doctor_appointments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='end_time',
            field=models.TimeField(blank=True, default=datetime.time(12, 45)),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='patient_docs',
            field=models.FileField(blank=True, default=None, upload_to='patient-docs'),
        ),
        migrations.AlterField(
            model_name='user',
            name='profile_picture',
            field=models.ImageField(blank=True, upload_to='profile_pics/'),
        ),
        migrations.AlterField(
            model_name='user',
            name='profile_type',
            field=models.CharField(choices=[('patient', 'Patient'), ('doctor', 'Doctor')], default='patient', max_length=10),
        ),
    ]
