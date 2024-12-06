#===----------------------------------------------------------------------===#
#
#         STAIRLab -- STructural Artificial Intelligence Laboratory
#
#===----------------------------------------------------------------------===#
#
#   Summer 2023, BRACE2 Team
#   Berkeley, CA
#
#----------------------------------------------------------------------------#
from django.db import models
from django.core.validators import int_list_validator

class Corridor(models.Model):
    id       = models.BigAutoField(primary_key=True)
    name     = models.CharField(max_length=20)
    route    = models.CharField(max_length=100, blank=True)
    assets   = models.ManyToManyField('Asset', related_name='corridors')

    def __str__(self):
        return f"{self.name} ({self.assets.count()})"

class Asset(models.Model):
    id = models.BigAutoField(primary_key=True)
    cesmd = models.CharField(max_length=7, blank=True, null=True)
    calid = models.CharField(max_length=15)
    name  = models.CharField(max_length=100, blank=True)

    is_complete = models.BooleanField(help_text="Is the asset a complete digital twin")

    nbi_data  = models.JSONField(default=dict, blank=True)
    cgs_data  = models.JSONField(default=list, blank=True)

    # Ground motion sensors
    ground_sensors = models.CharField(validators=[int_list_validator],
                                      max_length=200, blank=True,
                                      help_text="Comma-separated list of ground channel numbers")
    bridge_sensors = models.CharField(validators=[int_list_validator],
                                      max_length=200, blank=True,
                                      help_text="Comma-separated list of bridge channel numbers")

    def __str__(self):
        return f"{self.calid} - {self.name}"

    @property
    def predictors(self): # ->Dict[str, Predictor]:
        from irie.apps.prediction.predictor import PREDICTOR_TYPES
        from irie.apps.prediction.models import PredictorModel
        return {
            p.name: PREDICTOR_TYPES[p.protocol](p)
            for p in PredictorModel.objects.filter(asset=self)
        }

    @property
    def coordinates(self):
        if self.nbi_data:
            for table in self.nbi_data.values():
                if "Latitude" in table:
                    return map(float, map(table.get, ["Latitude", "Longitude"]))

        if self.cgs_data:
            lat, lon = map(self.cgs_data[0].get, ["Latitude", "Longitude"])
            return (float(lat.replace("N", "")), -float(lon.replace("W", "")))

        
        return (None, None)

    class Meta:
        ordering = ["-id"]

