#===----------------------------------------------------------------------===#
#
#         STAIRLab -- STructural Artificial Intelligence Laboratory
#
#===----------------------------------------------------------------------===#
from django.contrib import admin
from .models import Asset, Corridor

admin.site.register(Corridor)
admin.site.register(Asset)
