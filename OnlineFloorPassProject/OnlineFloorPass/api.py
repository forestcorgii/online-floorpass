from rest_framework import generics
from rest_framework.decorators import api_view

from .models import FloorPass, User, Log
from .serializers import FloorPassSerializer, LogSerializer, UserSerializer
from django.http import JsonResponse, HttpResponse

from rest_framework.response import Response
from rest_framework.reverse import reverse

# @api_view(['GET', 'POST'])
# def ReferenceID(request):
#     if request.method == 'GET':
#         floorpass = FloorPass.objects.get(pk=request.GET['id'])
#         serializer = FloorPassDetailSerializer(floorpass)
#         return JsonResponse(serializer.data)
#     elif request.method == 'POST':
#         floorpass = FloorPass.objects.get(pk=request.GET['id'])


@api_view(['GET'])
def api_root(request):
    if request.method == 'GET':
        floorpass = FloorPass.objects.all()

        if request.GET.get('supervisor_id', False):
            floorpass = floorpass.filter(
                supervisor_id=request.GET['supervisor_id'])
        else:
            if request.GET.get('department', False):
                floorpass = floorpass.filter(
                    department=request.GET['department'])
            if request.GET.get('location', False):
                floorpass = floorpass.filter(location=request.GET['location'])

        if request.GET.get('sort', False):
            floorpass = floorpass.order_by(request.GET['sort'])

        if request.GET.get('limit', False):
            floorpass = floorpass[:int(request.GET['limit'])]

        serializer = FloorPassSerializer(floorpass, many=True)
        return JsonResponse(serializer.data, safe=False)


class FloorPassList(generics.ListCreateAPIView):
    queryset = FloorPass.objects.order_by('-latest_log_date')
    serializer_class = FloorPassSerializer


class FloorPassDetail(generics.RetrieveUpdateAPIView):
    queryset = FloorPass.objects.all()
    serializer_class = FloorPassSerializer


class LogList(generics.ListCreateAPIView):
    queryset = Log.objects.all()
    serializer_class = LogSerializer


class LogDetail(generics.RetrieveUpdateAPIView):
    queryset = Log.objects.all()
    serializer_class = LogSerializer


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_fields = ['employee_id']


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
