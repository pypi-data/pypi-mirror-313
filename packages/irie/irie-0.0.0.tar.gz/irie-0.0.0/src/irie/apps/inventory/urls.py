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
from django.urls import path, re_path
from apps.inventory import views

urlpatterns = [
    path("dashboard/",     views.dashboard, name="dashboard"),
    path("dashboard.html", views.dashboard),
    path("dashboard/demo", views.dashboard),

    path("asset-table.html", views.asset_table),
    path("asset-table/", views.asset_table, name="asset_table"),
    re_path(
        r"^evaluations/(?P<event>[0-9 A-Z-]*)/(?P<cesmd>[0-9 A-Z-]*)/.*", views.asset_event_summary, name="asset_event_summary"
    ),
    re_path(r"^inventory/(?P<calid>[0-9 A-Z-]*)/", views.asset_profile, name="asset_profile"),
]
