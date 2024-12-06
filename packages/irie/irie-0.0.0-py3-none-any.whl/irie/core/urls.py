#===----------------------------------------------------------------------===#
#
#         STAIRLab -- STructural Artificial Intelligence Laboratory
#
#===----------------------------------------------------------------------===#
#
#   Fall 2022
#
#----------------------------------------------------------------------------#

from django.contrib import admin
from django.urls import path, include

admin.site.site_header = "BRACE2 Administration"
admin.site.index_title = "BRACE2 Administration"
admin.site.site_title  = "BRACE2 Administration"

urlpatterns = [
    path('admin/', admin.site.urls),

    # Authentication routes
    path("", include("apps.authentication.urls")),

    # Application routes
    path("", include("apps.events.urls")),

    path("", include("apps.evaluation.urls")),

    path("", include("apps.prediction.urls")),

    path("", include("apps.inventory.urls")),

    path("", include("apps.networks.urls")),

    path("", include("apps.documents.urls")),

    # Leave `site.urls` as last the last line
    path("", include("apps.site.urls"))
]
