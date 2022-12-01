# Generated by Django 4.1.3 on 2022-12-01 16:52

import api.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Ultima Atualização')),
                ('deleted_at', models.DateTimeField(auto_now_add=True, verbose_name='Data de Exclusão')),
                ('cep', models.CharField(max_length=10, verbose_name='Cep')),
                ('logradouro', models.CharField(max_length=255, verbose_name='Logradouro')),
                ('complemento', models.CharField(max_length=255, verbose_name='Complemento')),
                ('bairro', models.CharField(max_length=255, verbose_name='Bairro')),
                ('localidade', models.CharField(max_length=255, verbose_name='Cidade')),
                ('uf', models.CharField(max_length=2, verbose_name='Estado')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
            ],
            options={
                'verbose_name': 'Address',
                'verbose_name_plural': 'Addresses',
                'db_table': 'tbl_address',
            },
        ),
        migrations.CreateModel(
            name='HourAvailable',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Ultima Atualização')),
                ('deleted_at', models.DateTimeField(auto_now_add=True, verbose_name='Data de Exclusão')),
                ('hourAvailable', models.CharField(max_length=8, verbose_name='Hora Serviço')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
            ],
            options={
                'verbose_name': 'Hour Available',
                'verbose_name_plural': 'Hour Availables',
                'db_table': 'tbl_hour',
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Ultima Atualização')),
                ('deleted_at', models.DateTimeField(auto_now_add=True, verbose_name='Data de Exclusão')),
                ('image', models.ImageField(blank=True, null=True, upload_to=api.models.Service.get_file_path, verbose_name='Imagem')),
                ('name', models.CharField(max_length=255, verbose_name='Titulo')),
                ('description', models.TextField(verbose_name='Descrição')),
            ],
            options={
                'verbose_name': 'Service',
                'verbose_name_plural': 'Services',
                'db_table': 'tbl_service',
            },
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Ultima Atualização')),
                ('deleted_at', models.DateTimeField(auto_now_add=True, verbose_name='Data de Exclusão')),
                ('brand', models.CharField(max_length=255, verbose_name='Marca Veículo')),
                ('model', models.CharField(max_length=255, verbose_name='Modelo Veículo')),
                ('fuell', models.CharField(max_length=255, verbose_name='Combustível')),
                ('year', models.CharField(max_length=4, verbose_name='Ano Fabricação')),
                ('odomitter', models.CharField(max_length=9, verbose_name='Hodometro')),
                ('plate', models.CharField(max_length=10, verbose_name='Placa Veículo')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
            ],
            options={
                'verbose_name': 'vehicle',
                'verbose_name_plural': 'vehicles',
                'db_table': 'tbl_vehicle',
            },
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Ultima Atualização')),
                ('deleted_at', models.DateTimeField(auto_now_add=True, verbose_name='Data de Exclusão')),
                ('day', models.DateField(help_text='Escolha data disponível', verbose_name='Data do Serviço')),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='Address', related_query_name='Addres', to='api.address', verbose_name='Endereço')),
                ('hour', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='HourAvailable', related_query_name='HourAvailable', to='api.houravailable', verbose_name='Hora')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='Service', related_query_name='Service', to='api.service', verbose_name='Serviço')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='Vehicle', related_query_name='Vehicle', to='api.vehicle', verbose_name='Veículo')),
            ],
            options={
                'verbose_name': 'Schedule',
                'verbose_name_plural': 'Schedules',
                'db_table': 'tbl_schedule',
            },
        ),
    ]