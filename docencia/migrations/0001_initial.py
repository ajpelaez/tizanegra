# Generated by Django 2.0.2 on 2018-04-25 12:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Asignatura',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Asignaturas',
            },
        ),
        migrations.CreateModel(
            name='Profesor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('foto', models.ImageField(blank=True, null=True, upload_to='static/')),
                ('email', models.EmailField(max_length=200)),
                ('asignaturas', models.ManyToManyField(to='docencia.Asignatura')),
            ],
            options={
                'verbose_name_plural': 'Profesores',
            },
        ),
        migrations.CreateModel(
            name='Titulacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Titulaciones',
            },
        ),
        migrations.CreateModel(
            name='Universidad',
            fields=[
                ('siglas', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='static/')),
                ('web', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name_plural': 'Universidades',
            },
        ),
        migrations.AddField(
            model_name='titulacion',
            name='universidad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='docencia.Universidad'),
        ),
        migrations.AddField(
            model_name='profesor',
            name='universidad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='docencia.Universidad'),
        ),
        migrations.AddField(
            model_name='asignatura',
            name='titulaciones',
            field=models.ManyToManyField(to='docencia.Titulacion'),
        ),
        migrations.AddField(
            model_name='asignatura',
            name='universidad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='docencia.Universidad'),
        ),
    ]
