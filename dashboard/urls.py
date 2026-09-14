from django.urls import path

from .views import (
    browse_save,
    communication,
    communication_data,
    create_racer,
    dashboard,
    export_model_csv,
    export_model_json,
    race_detail,
    race_history,
    reports,
    update_rig,
)

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('races/<int:pk>/', race_detail, name='race-detail'),
    path('race-history/', race_history, name='race-history'),
    path('reports/', reports, name='reports'),
    path('browse-save/', browse_save, name='browse-save'),
    path('communication/', communication, name='communication'),
    path('communication/data/', communication_data, name='communication-data'),
    path('rigs/<int:pk>/update/', update_rig, name='update-rig'),
    path('racers/create/', create_racer, name='create-racer'),
    path('browse-save/export/<str:model_name>/csv/', export_model_csv, name='export-model-csv'),
    path('browse-save/export/<str:model_name>/json/', export_model_json, name='export-model-json'),
]
