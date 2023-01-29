from rest_framework import serializers
from clientes import models

from rest_framework import serializers
from clientes.models import Clientes

class ClientesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clientes
        fields = ['id_cliente', 'nome', 'cpf', 'telefone', 'genero', 'cep', 'cidade', 'estado', 'logradouro']
