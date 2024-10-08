# Generated by Django 5.0.3 on 2024-08-27 20:01

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Obra',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('cod', models.IntegerField(default=0)),
                ('descripcion', models.CharField(max_length=100)),
                ('fechaCreacion', models.DateTimeField(auto_now_add=True)),
                ('direccionCalle', models.CharField(max_length=100)),
                ('direccionNumero', models.IntegerField(default=0)),
                ('tipoObra', models.CharField(max_length=2)),
                ('idUsuario', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ObraUsuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaCreacion', models.DateTimeField(auto_now_add=True)),
                ('estado', models.IntegerField(default=1)),
                ('obra', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='obra', to='Tratos.obra')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TipoUnidad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cod', models.CharField(max_length=10)),
                ('descripcion', models.CharField(max_length=50)),
                ('medicion', models.CharField(max_length=3)),
                ('fechaCreacion', models.DateTimeField(auto_now_add=True)),
                ('estado', models.IntegerField(default=1)),
                ('idUsuario', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('obra', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Tratos.obra')),
            ],
            options={
                'unique_together': {('cod', 'descripcion')},
            },
        ),
        migrations.CreateModel(
            name='TratoCapataz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('apellido', models.CharField(max_length=50)),
                ('fechaCreacion', models.DateTimeField(auto_now_add=True)),
                ('idObra', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Tratos.obra')),
                ('idUsuario', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('id', 'nombre')},
            },
        ),
        migrations.CreateModel(
            name='TratoCategoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cod', models.CharField(max_length=10)),
                ('descripcion', models.CharField(max_length=50)),
                ('fechaCreacion', models.DateTimeField(auto_now_add=True)),
                ('idUsuario', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('cod', 'descripcion')},
            },
        ),
        migrations.CreateModel(
            name='ObraCategoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaCreacion', models.DateTimeField(auto_now_add=True)),
                ('estado', models.IntegerField(default=1)),
                ('obra', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='obrac', to='Tratos.obra')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='categoria', to='Tratos.tratocategoria')),
            ],
        ),
        migrations.CreateModel(
            name='TratoEspecialidad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cod', models.CharField(max_length=10)),
                ('descripcion', models.CharField(max_length=50)),
                ('fechaCreacion', models.DateTimeField(auto_now_add=True)),
                ('idUsuario', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('cod', 'descripcion')},
            },
        ),
        migrations.CreateModel(
            name='UnidadMedida',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cod', models.CharField(max_length=10)),
                ('descripcion', models.CharField(max_length=50)),
                ('fechaCreacion', models.DateTimeField(auto_now_add=True)),
                ('idUsuario', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('cod', 'descripcion')},
            },
        ),
        migrations.CreateModel(
            name='Trato',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('cod', models.CharField(max_length=10)),
                ('codFamilia', models.CharField(max_length=15)),
                ('partida', models.TextField(blank=True)),
                ('nroMaestros', models.IntegerField(default=0)),
                ('nroAyudantes', models.IntegerField(default=0)),
                ('nroJornales', models.IntegerField(default=0)),
                ('sueldoMaestro', models.IntegerField(default=0)),
                ('sueldoAyudante', models.IntegerField(default=0)),
                ('sueldoJornal', models.IntegerField(default=0)),
                ('valorCuadrilla', models.IntegerField(default=0)),
                ('valorTrato', models.BigIntegerField(default=0)),
                ('cantidad', models.BigIntegerField(default=0)),
                ('fechaCreacion', models.DateTimeField(auto_now_add=True)),
                ('orden', models.IntegerField(blank=True, null=True, unique=True)),
                ('idUsuario', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('obra', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Tratos.obra')),
                ('capataz', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Tratos.tratocapataz')),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Tratos.tratocategoria')),
                ('especialidad', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Tratos.tratoespecialidad')),
                ('unidadMedida', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Tratos.unidadmedida')),
            ],
        ),
        migrations.CreateModel(
            name='UnidadModelo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cod', models.CharField(max_length=10)),
                ('descripcion', models.CharField(max_length=50)),
                ('fechaCreacion', models.DateTimeField(auto_now_add=True)),
                ('estado', models.IntegerField(default=1)),
                ('idObra', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Tratos.obra')),
                ('idUsuario', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('tipo', models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='Tratos.tipounidad')),
            ],
            options={
                'unique_together': {('cod', 'descripcion')},
            },
        ),
        migrations.CreateModel(
            name='TratoModelo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.BigIntegerField(default=0)),
                ('rendimiento', models.DecimalField(decimal_places=2, max_digits=8)),
                ('valorTratoModelo', models.BigIntegerField(default=0)),
                ('fechaCreacion', models.DateTimeField(auto_now_add=True)),
                ('estado', models.BooleanField()),
                ('idUsuario', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('trato', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Tratos.trato')),
                ('modelo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Tratos.unidadmodelo')),
            ],
        ),
        migrations.AddField(
            model_name='trato',
            name='Modelos',
            field=models.ManyToManyField(related_name='modelosTrato', through='Tratos.TratoModelo', to='Tratos.unidadmodelo'),
        ),
        migrations.CreateModel(
            name='UnidadObra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cod', models.CharField(max_length=10)),
                ('descripcion', models.CharField(max_length=50)),
                ('fechaCreacion', models.DateTimeField(auto_now_add=True)),
                ('estado', models.IntegerField(default=1)),
                ('idModelo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='modelos', to='Tratos.unidadmodelo')),
                ('idObra', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Tratos.obra')),
                ('idUsuario', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TratoUnidadBloqueada',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('motivo', models.CharField(max_length=100)),
                ('fechaCreacion', models.DateTimeField(auto_now_add=True)),
                ('estado', models.IntegerField(default=1)),
                ('idUsuario', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('trato', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Tratos.trato')),
                ('unidad', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Tratos.unidadobra')),
            ],
        ),
    ]
