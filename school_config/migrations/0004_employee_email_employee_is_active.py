# Generated by Django 4.0.3 on 2022-06-03 01:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school_config', '0003_grade_group_employee_school_gradegroupconfig_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
