from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Device, Rig
from .serializers import DeviceSerializer, RigSerializer


class DeviceHealthView(APIView):
    def get(self, request):
        return Response({'status': 'ok', 'devices': []})


class DeviceListView(APIView):
    def get(self, request):
        return Response(DeviceSerializer(Device.objects.select_related('rig'), many=True).data)


class RigViewSet(viewsets.ModelViewSet):
    queryset = Rig.objects.prefetch_related('devices').all()
    serializer_class = RigSerializer


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.select_related('rig').all()
    serializer_class = DeviceSerializer
