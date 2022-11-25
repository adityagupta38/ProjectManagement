from rest_framework import viewsets
from proj.models import Clients, Projects
from .serializers import ClientSerializer, ProjectSerializer
from rest_framework.response import Response


class ClientsApi(viewsets.ViewSet):
    def list(self, request):
        queryset = Clients.objects.all()
        serializer = ClientSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response( serializer.data)
        return Response( serializer.errors)

    def retrieve(self, request, pk):
        client = Clients.objects.get(id=pk)
        clproj = client.project.all()
        cserializer = ClientSerializer(client)
        projserializer = ProjectSerializer(clproj, many=True)
        return Response({'client': cserializer.data,
                         'projects': projserializer.data})


    def partial_update(self, request, pk):
            client = Clients.objects.get(id=pk)
            serializer = ClientSerializer(client, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)

    def destroy(self, request, pk):
        client = Clients.objects.get(id=pk)
        status, deleted_client = client.delete()
        if status == 1:
            return Response({'msg': 'Client Deleted Successfully'})
        return Response({'msg': 'Unable to delete pls try again'})


class ProjectsApi(viewsets.ViewSet):

    def list(self, request):
        projects = Projects.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def update(self, request, pk):
        client = Clients.objects.get(id=pk)
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            proj = serializer.save(client=client)
            client_obj = proj.client
            clserializer = ClientSerializer(client_obj)
            users_list = proj.users.all()
            return Response( {'project': serializer.data, 'client': clserializer.data, 'users': users_list})
        return Response( serializer.errors)