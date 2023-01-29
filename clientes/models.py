from xml.dom import ValidationErr
from django.db import models
from uuid import uuid4

def validate_cpf(value):
    if len(value) != 11:
        raise ValidationErr("CPF deve conter 11 dígitos.")

class Clientes(models.Model):
    id_cliente = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    nome = models.CharField(max_length=255)
    cpf = models.CharField(max_length=11, validators=[validate_cpf])
    telefone =  models.IntegerField()
    genero =  models.CharField(max_length=10)
    cep =  models.IntegerField()
    cidade =  models.CharField(max_length=255, editable=False)
    estado =  models.CharField(max_length=255, editable=False)
    logradouro =  models.CharField(max_length=255, editable=False)