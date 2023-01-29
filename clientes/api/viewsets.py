import requests
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from clientes.models import Clientes
from clientes.api.serializers import ClientesSerializer

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Clientes.objects.all()
    serializer_class = ClientesSerializer
    http_method_names = ['get', 'post', 'put', 'delete']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        cep = request.data.get('cep')
        response = requests.get(f'https://viacep.com.br/ws/{cep}/json/')
        address_data = response.json()
        serializer.is_valid(raise_exception=True)
        serializer.validated_data.update({
            'cidade': address_data['localidade'],
            'estado': address_data['uf'],
            'logradouro': address_data['logradouro']
        })
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=response.status_code, headers=headers)
        
    def get_queryset(self):
        queryset = self.queryset
        cpf = self.request.query_params.get('cpf', None)
        cep = self.request.query_params.get('cep', None)
        nome = self.request.query_params.get('nome', None)

        if cpf is not None:
            queryset = queryset.filter(cpf=cpf)
        if cep is not None:
            queryset = queryset.filter(cep=cep)
        if nome is not None:
            queryset = queryset.filter(nome__icontains=nome)

        return queryset

    def delete_queryset(self, request, *args, **kwargs):
        client = self.get_object()
        client.delete()
        return Response({"message": "Client deleted successfully"})

    def update_queryset(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_update(self, serializer):
     serializer.save()

