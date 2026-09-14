from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

admin.site.site_header = 'SIM RACING CONTROL CENTER'
admin.site.site_title = 'Race Control Admin'
admin.site.index_title = 'Race Control Administration'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/devices/', include('devices.urls')),
    path('api/races/', include('races.urls')),
    path('', include('dashboard.urls')),
    path('', RedirectView.as_view(pattern_name='dashboard', permanent=False)),
]
