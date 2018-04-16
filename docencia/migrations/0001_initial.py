# Generated by Django 2.0.3 on 2018-04-16 19:58

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
        ),
        migrations.CreateModel(
            name='Profesor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('foto', models.ImageField(blank=True, null=True, upload_to='static/')),
                ('email', models.EmailField(max_length=200)),
                ('asignaturas', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='docencia.Asignatura')),
            ],
        ),
        migrations.CreateModel(
            name='Titulacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Universidad',
            fields=[
                ('nombre', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='static/')),
                ('web', models.CharField(max_length=200)),
            ],
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
            name='titulacion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='docencia.Titulacion'),
        ),
        migrations.AddField(
            model_name='asignatura',
            name='universidad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='docencia.Universidad'),
        ),
    ]
