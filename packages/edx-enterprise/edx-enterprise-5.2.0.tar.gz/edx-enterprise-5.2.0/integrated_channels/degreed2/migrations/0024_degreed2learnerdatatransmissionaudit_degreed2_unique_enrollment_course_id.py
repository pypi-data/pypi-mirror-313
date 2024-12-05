# Generated by Django 3.2.22 on 2024-02-06 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('degreed2', '0023_alter_historicaldegreed2enterprisecustomerconfiguration_options'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='degreed2learnerdatatransmissionaudit',
            constraint=models.UniqueConstraint(fields=('enterprise_course_enrollment_id', 'course_id'), name='degreed2_unique_enrollment_course_id'),
        ),
    ]
