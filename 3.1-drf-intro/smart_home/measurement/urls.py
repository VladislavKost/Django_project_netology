from django.urls import path
from .views import SensorView, MeasurementView, UpdateSensorView

urlpatterns = [
    path("sensors/", SensorView.as_view()),
    path("sensors/<pk>/", UpdateSensorView.as_view()),
    path("measurements/", MeasurementView.as_view()),
]
