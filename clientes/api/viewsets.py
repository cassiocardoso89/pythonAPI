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

    def get_queryset(self):
        queryset = self.queryset
        cpf = self.request.query_params.get('cpf')
        cep = self.request.query_params.get('cep')
        nome = self.request.query_params.get('nome')

        if cpf:
            queryset = queryset.filter(cpf=cpf)
        if cep:
            queryset = queryset.filter(cep=cep)
        if nome:
            queryset = queryset.filter(nome__icontains=nome)

        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        cep = request.data.get('cep')
        if not cep:
            return Response({"CEP não informado"}, status=Response.status_code)
        try:
            response = requests.get(f'https://viacep.com.br/ws/{cep}/json/')
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            return Response(serializer.data,  {"" : str(e)}, status=Response.status_code)
        
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
        return Response(serializer.data, status=Response.status_code, headers=headers)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        cep = request.data.get('cep')
        if not cep:
            return Response({"CEP não informado"}, status=Response.status_code)
        try:
            response = requests.get(f'https://viacep.com.br/ws/{cep}/json/')
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            return Response(instance, {"" : str(e)}, status=Response.status_code)
        address_data = response.json()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.validated_data.update({
                'cidade': address_data['localidade'],
                'estado': address_data['uf'],
                'logradouro': address_data['logradouro']
            })
        if not serializer.is_valid():
            return Response(serializer.data,  {"" : str(e)}, status=Response.status_code)

        self.perform_update(serializer)
        return Response(serializer.data, status=Response.status_code)
        
    def perform_update(self, serializer):
            serializer.save()

    def delete_queryset(self, request, *args, **kwargs):
        try:
            client = self.get_object()
            client.delete()
            return Response({"Cliente removido com sucesso"})
        except Exception as e:
            return Response(request.data,  {"" : str(e)}, status=Response.status_code)


