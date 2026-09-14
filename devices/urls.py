from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import DeviceHealthView, DeviceListView, DeviceViewSet, RigViewSet

app_name = 'devices'

router = DefaultRouter()
router.register('rigs', RigViewSet, basename='rig')
router.register('items', DeviceViewSet, basename='device')

urlpatterns = [
    path('', include(router.urls)),
    path('', DeviceListView.as_view(), name='list'),
    path('health/', DeviceHealthView.as_view(), name='health'),
]
