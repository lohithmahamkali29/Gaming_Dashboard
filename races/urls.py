from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import RaceEntryViewSet, RaceListView, RaceStartView, RaceTelemetryView, RaceViewSet

app_name = 'races'

router = DefaultRouter()
router.register('entries', RaceEntryViewSet, basename='entry')
router.register('', RaceViewSet, basename='race')

urlpatterns = [
    path('<int:pk>/start/', RaceStartView.as_view(), name='start'),
    path('<int:pk>/telemetry/', RaceTelemetryView.as_view(), name='telemetry'),
    path('', include(router.urls)),
    path('', RaceListView.as_view(), name='list'),
]
