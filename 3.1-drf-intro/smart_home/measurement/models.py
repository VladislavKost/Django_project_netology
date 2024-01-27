from django.db import models

from django.db import models


class Sensor(models.Model):

    name = models.CharField(max_length=50, verbose_name="Sensor name")
    description = models.CharField(max_length=250, verbose_name="Sensor description")

    class Meta:
        ordering = ["pk"]


class Measurement(models.Model):

    sensor_id = models.ForeignKey(
        Sensor, on_delete=models.CASCADE, related_name="measurements"
    )
    temperature = models.FloatField()
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["pk"]
