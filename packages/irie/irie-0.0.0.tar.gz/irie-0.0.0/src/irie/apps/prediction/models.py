#===----------------------------------------------------------------------===#
#
#         STAIRLab -- STructural Artificial Intelligence Laboratory
#
#===----------------------------------------------------------------------===#
from django.db import models

from apps.inventory.models import Asset

class PredictorModel(models.Model):
    # https://docs.djangoproject.com/en/4.2/ref/models/fields/
    class Protocol(models.TextChoices):
        TYPE1 = "BRACE2_CLI_PREDICTOR_V1"
        TYPE2 = "BRACE2_CLI_PREDICTOR_T2"
        TYPE3 = "BRACE2_CLI_PREDICTOR_T3"
        TYPE4 = "BRACE2_CLI_PREDICTOR_T4"

    id          = models.BigAutoField(primary_key=True)
    name        = models.CharField(max_length=35)
    asset       = models.ForeignKey(Asset, on_delete=models.CASCADE)
    description = models.TextField(default="")

    protocol    = models.CharField(max_length=25, 
                                   choices=Protocol.choices, 
                                   default=Protocol.TYPE2)

    entry_point = models.JSONField(default=list)
    config      = models.JSONField(default=dict)
    config_file = models.FileField(upload_to='predictor_configs/', null=True, blank=True)
    render_file = models.FileField(upload_to='renderings/', null=True, blank=True)
    metrics     = models.JSONField(default=list)

    active      = models.BooleanField()

    def __str__(self):
        return f"{self.asset.calid} - {self.name} : {self.description}"

