# Generated by Django 4.0.3 on 2022-05-31 02:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school_config', '0002_position_employee'),
        ('efile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='efile',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='school_config.employee'),
        ),
    ]
