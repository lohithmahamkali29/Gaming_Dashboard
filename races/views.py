from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Race, RaceEntry
from .serializers import RaceEntrySerializer, RaceSerializer
from .services.engine import RaceEngine


class RaceListView(APIView):
    def get(self, request):
        return Response(RaceSerializer(Race.objects.prefetch_related('entries'), many=True).data)


class RaceViewSet(viewsets.ModelViewSet):
    queryset = Race.objects.prefetch_related('entries').all()
    serializer_class = RaceSerializer


class RaceEntryViewSet(viewsets.ModelViewSet):
    queryset = RaceEntry.objects.select_related('race', 'rig').all()
    serializer_class = RaceEntrySerializer


class RaceStartView(APIView):
    def post(self, request, pk):
        race = Race.objects.get(pk=pk)
        return Response(RaceSerializer(RaceEngine().start(race)).data)


class RaceTelemetryView(APIView):
    def get(self, request, pk):
        race = Race.objects.prefetch_related('entries__rig').get(pk=pk)
        RaceEngine().tick(race)
        race.entries.all()._result_cache = None
        return Response(RaceSerializer(race).data)
