from django.contrib.gis.db import models

class Peak(models.Model):
    """
    Represents a mountain peak
    """
    name = models.CharField(max_length=100)
    location = models.PointField()
    altitude = models.FloatField()

    def __str__():
        return self.name + self.altitude
