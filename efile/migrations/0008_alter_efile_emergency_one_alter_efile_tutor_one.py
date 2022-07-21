# Generated by Django 4.0.3 on 2022-07-20 18:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('efile', '0007_remove_efile_academic_year_remove_efile_school_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='efile',
            name='emergency_one',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='emergency_one', to='efile.tutor'),
        ),
        migrations.AlterField(
            model_name='efile',
            name='tutor_one',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tutor_one', to='efile.tutor'),
        ),
    ]
