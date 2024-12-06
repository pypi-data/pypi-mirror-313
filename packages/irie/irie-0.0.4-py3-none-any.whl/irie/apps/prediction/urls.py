#===----------------------------------------------------------------------===#
#
#         STAIRLab -- STructural Artificial Intelligence Laboratory
#
#===----------------------------------------------------------------------===#
#
#   Author: Claudio Perez
#
#----------------------------------------------------------------------------#
from django.urls import path, re_path
from .views import new_prediction, asset_predictors, predictor_profile, predictor_upload

urlpatterns = [
    re_path("^inventory/[0-9 A-Z-]*/predictors/new",   new_prediction),
    re_path("^inventory/[0-9 A-Z-]*/predictors/[0-9]", predictor_profile),
    re_path("upload/", predictor_upload),
    re_path("^inventory/[0-9 A-Z-]*/predictors/",      asset_predictors, name="asset_predictors"),
    re_path("^inventory/[0-9 A-Z-]*/predictors/",      asset_predictors),
]
