#===----------------------------------------------------------------------===#
#
#         STAIRLab -- STructural Artificial Intelligence Laboratory
#
#===----------------------------------------------------------------------===#
#
#   Fall 2024, BRACE2 Team
#
#   Berkeley, CA
#
#----------------------------------------------------------------------------#
from django.urls import path
from apps.networks import views

urlpatterns = [
    path("networks/",     views.network_maps,     name="networks"),
    path("api/networks/", views.load_network_map, name='load_network_map'),
]
