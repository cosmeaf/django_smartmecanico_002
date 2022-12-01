import os
import uuid
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model();

class Base(models.Model):
    id = models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
    created_at = models.DateTimeField('Data de Criação', auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField('Ultima Atualização', auto_now=True, auto_now_add=False)
    deleted_at = models.DateTimeField('Data de Exclusão', auto_now=False, auto_now_add=True)

    class Meta:
        abstract = True
        verbose_name = 'Base Model'
        verbose_name_plural = 'Bases Models'
        
################### PROFILE MODEL ###################
class Profile(models.Model):
    def get_file_path(instance, filename):
        ext = filename.split('.')[-1]
        filename = "%s.%s" % (uuid.uuid4(), ext)
        return os.path.join('icon', filename)
    user = models.ForeignKey(User, verbose_name='Usuário', on_delete=models.CASCADE)
    image = models.ImageField('Fotografia', default='default.png', upload_to=get_file_path, blank=True, null=True)
    phone_number = models.CharField('Celular', max_length=13, null=True, blank=True)
    birthdate = models.DateField('Data Nascimento',null=True, blank=True)
    biography = models.TextField('Biografia', editable=True, null=True, blank=True)

    def __str__(self):  # __unicode__ for Python 2
        return self.user.username
          
################### ADDRESS MODEL ###################
class Address(Base):
    user = models.ForeignKey(User, verbose_name='Usuário', on_delete=models.CASCADE)
    cep = models.CharField('Cep', max_length=10)
    logradouro = models.CharField('Logradouro', max_length=255, blank=False, null=False)
    complemento = models.CharField('Complemento', max_length=255, blank=False, null=False)
    bairro = models.CharField('Bairro', max_length=255, blank=False, null=False)
    localidade = models.CharField('Cidade', max_length=255, blank=False, null=False)
    uf = models.CharField('Estado', max_length=2, blank=False, null=False)
    
    class Meta:
        db_table = 'tbl_address'
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'

    def __str__(self):
        return f'{self.cep}'
      
################### VEHICLE MODEL ###################
class Vehicle(Base):
    """Model definition for Vehicle."""
    brand = models.CharField(
        'Marca Veículo', max_length=255, blank=False, null=False)
    model = models.CharField(
        'Modelo Veículo', max_length=255, blank=False, null=False)
    fuell = models.CharField(
        'Combustível', max_length=255, blank=False, null=False)
    year = models.CharField(
        'Ano Fabricação', max_length=4, blank=False, null=False)
    odomitter = models.CharField(
        'Hodometro', max_length=9, blank=False, null=False)
    plate = models.CharField(
        'Placa Veículo', max_length=10, blank=False, null=False)
    user = models.ForeignKey(
        User, verbose_name='Usuário', on_delete=models.CASCADE)

    class Meta:
        """Meta definition for Vehicle."""
        db_table = 'tbl_vehicle'
        verbose_name = 'vehicle'
        verbose_name_plural = 'vehicles'

    def __str__(self):
        """Unicode representation of Vehicle."""
        return self.brand

################### SERVICES MODEL ###################
class Service(Base):
    def get_file_path(instance, filename):
        ext = filename.split('.')[-1]
        filename = "%s.%s" % (uuid.uuid4(), ext)
        return os.path.join('icon', filename)

    image = models.ImageField(
        'Imagem', upload_to=get_file_path, blank=True, null=True)
    name = models.CharField('Titulo', max_length=255, editable=True)
    description = models.TextField(
        'Descrição', editable=True)

    class Meta:
        db_table = 'tbl_service'
        verbose_name = 'Service'
        verbose_name_plural = 'Services'

    def __str__(self):
        return f'{self.name}'

################### AVAILABLE HOUR MODEL ###################
class HourAvailable(Base):
    user = models.ForeignKey(
        User, verbose_name='Usuário', on_delete=models.CASCADE)
    hourAvailable = models.CharField('Hora Serviço', max_length=8)

    class Meta:
        db_table = 'tbl_hour'
        verbose_name = 'Hour Available'
        verbose_name_plural = 'Hour Availables'

    def __str__(self):
        return f'{self.hourAvailable}'

################### SCHEDULE MODEL ###################    
class Schedule(Base):
    user = models.ForeignKey(
        User, verbose_name='Usuário', on_delete=models.CASCADE)
    address = models.ForeignKey(Address, verbose_name='Endereço', on_delete=models.PROTECT,
                                related_name='Address', related_query_name="Addres")
    vehicle = models.ForeignKey(Vehicle, verbose_name='Veículo', on_delete=models.PROTECT,
                                related_name='Vehicle', related_query_name="Vehicle")
    service = models.ForeignKey(Service, verbose_name='Serviço', on_delete=models.PROTECT,
                                related_name='Service', related_query_name="Service")
    hour = models.ForeignKey(HourAvailable, verbose_name='Hora', on_delete=models.PROTECT,
                             related_name='HourAvailable', related_query_name="HourAvailable")
    day = models.DateField('Data do Serviço', help_text='Escolha data disponível')

    class Meta:
        db_table = 'tbl_schedule'
        verbose_name = 'Schedule'
        verbose_name_plural = 'Schedules'

    def __str__(self):
        return f'{self.service}'
