#===----------------------------------------------------------------------===#
#
#         STAIRLab -- STructural Artificial Intelligence Laboratory
#
#===----------------------------------------------------------------------===#
#
#   This module implements the "Configure Predictors" page
#
#   Author: Claudio Perez
#
#----------------------------------------------------------------------------#
import os
import json

from django.shortcuts import HttpResponse
from django.template import loader, TemplateDoesNotExist
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from irie.apps.site.view_utils import raise404
from irie.apps.inventory.models import Asset
from irie.apps.prediction.predictor import PREDICTOR_TYPES, OpenSeesRunner
from irie.apps.prediction.models import PredictorModel
from .forms import PredictorForm

@login_required(login_url="/login/")
def new_prediction(request):
    context = {}

    page_template = "form-submission.html" #request.path.split("/")[-1]
    context["segment"] = page_template
    html_template = loader.get_template("prediction/" + page_template)
    return HttpResponse(html_template.render(context, request))


#@login_required(login_url="/login/")
@api_view(["GET", "POST", "PUT"])
@permission_classes([IsAuthenticated])
def predictor_api(request):

    context = {"segment": "assets"}

    context["predictor_types"] = list(reversed([
           {"schema": json.dumps(cls.schema),
            "name":   cls.__name__,
            "title":  cls.schema["title"]}
            for cls in set(PREDICTOR_TYPES.values())
    ]))

    calid = request.path.split("/")[-3]

    try:
        context["asset"] = Asset.objects.get(calid=calid)

    except:
        return HttpResponse(
                loader.get_template("home/page-404-sidebar.html").render(context, request)
               )

    if request.method == "POST":
        PREDICTOR_TYPES["BRACE2_CLI_PREDICTOR_T2"].create(context["asset"],request).save()

    html_template = loader.get_template("prediction/asset-predictors.html")
    return HttpResponse(html_template.render(context, request))


# @api_view(["GET", "POST", "PUT"])
@login_required(login_url="/login/")
# @permission_classes([IsAuthenticated])
def asset_predictors(request):

    context = {"segment": "assets"}

    context["predictor_types"] = list(reversed([
           {"schema": json.dumps(cls.schema),
            "name":   cls.__name__,
            "title":  cls.schema.get("title", "NO TITLE")}
            for cls in set(PREDICTOR_TYPES.values())
    ]))

    calid = request.path.split("/")[-3]
    try:
        context["asset"] = Asset.objects.get(calid=calid)
    except:
        return HttpResponse(
                loader.get_template("home/page-404-sidebar.html").render(context, request)
               )

    if request.method == "POST":
        PREDICTOR_TYPES["BRACE2_CLI_PREDICTOR_T2"].create(context["asset"],request).save()

    html_template = loader.get_template("prediction/asset-predictors.html")
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def predictor_profile(request):

    context = {}
    html_template = loader.get_template("prediction/predictor-profile.html")
    context["segment"] = "assets"

    url_segs = request.path.split("/")
    if len(url_segs) < 5:
        return raise404(request, context)
    else:
        calid = url_segs[2]
        preid = url_segs[4]

    try:
        asset = Asset.objects.get(calid=calid)
    except ObjectDoesNotExist:
        return raise404(request, context)

    try:
        predictor = PredictorModel.objects.get(pk=int(preid))
    except ObjectDoesNotExist:
        return raise404(request, context)

    context["asset"] = asset
    context["predictor"] = PREDICTOR_TYPES[predictor.protocol](predictor)


    try:
        return HttpResponse(html_template.render(context, request))

    except TemplateDoesNotExist:
        context["rendering"] = None
        return HttpResponse(html_template.render(context, request))

    except Exception as e:
        if "DEBUG" in os.environ and os.environ["DEBUG"]:
            raise e
        html_template = loader.get_template("site/page-500.html")
        return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def predictor_upload(request):

    context = {}
    html_template = loader.get_template("prediction/predictor-upload.html")
    context["segment"] = "assets"

    context["title"] = "The Title"

    if request.method == 'POST':
        form = PredictorForm(request.POST, request.FILES)  # include request.FILES
        if form.is_valid():
            # Process the form data and uploaded file
            asset = form.cleaned_data['asset']
            uploaded_file = request.FILES['config_file']

            with open(uploaded_file.name, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            # Save the predictor
            OpenSeesRunner.create(asset,None,form).save()

            context = {}

            return render(request, 'prediction/predictor-upload.html',
                          context)
    else:
        form = PredictorForm()


    try:
        return render(request, 'prediction/predictor-upload.html', {'form': form})


    except Exception as e:
        if "DEBUG" in os.environ and os.environ["DEBUG"]:
            raise e
        html_template = loader.get_template("site/page-500.html")
        return HttpResponse(html_template.render(context, request))


