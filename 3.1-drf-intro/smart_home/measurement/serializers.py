from rest_framework.serializers import ModelSerializer
from .models import Sensor, Measurement


class MeasurementSerializer(ModelSerializer):
    class Meta:
        model = Measurement
        fields = ["sensor_id", "temperature", "created_at"]


class SensorDetailSerializer(ModelSerializer):
    measurements = MeasurementSerializer(read_only=True, many=True)

    class Meta:
        model = Sensor
        fields = ["id", "name", "description", "measurements"]


class SensorSerializer(ModelSerializer):
    class Meta:
        model = Sensor
        fields = ["id", "name", "description"]
