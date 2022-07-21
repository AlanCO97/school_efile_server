# Generated by Django 4.0.3 on 2022-05-30 23:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AcademicYear',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('init_day', models.DateField()),
                ('end_day', models.DateField()),
            ],
            options={
                'verbose_name': 'Ciclo escolar',
                'verbose_name_plural': 'Ciclos escolares',
            },
        ),
        migrations.CreateModel(
            name='SchoolTurns',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('turn', models.CharField(choices=[('MATUTINO', 'Matutino'), ('VESPERTINO', 'Vespertino')], default='VESPERTINO', max_length=20)),
            ],
            options={
                'verbose_name': 'Turno de la escuela',
                'verbose_name_plural': 'Turnos de la escuela',
            },
        ),
        migrations.CreateModel(
            name='SchoolConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school_name', models.CharField(max_length=255)),
                ('school_key', models.CharField(max_length=60)),
                ('zone', models.CharField(blank=True, max_length=255, null=True)),
                ('turn', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school_config.schoolturns')),
            ],
            options={
                'verbose_name': 'Configuracion de la escuela',
                'verbose_name_plural': 'Configuraciones de la escuela',
            },
        ),
    ]