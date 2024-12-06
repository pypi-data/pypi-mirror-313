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
import os
import re
from django.core.paginator import Paginator
from django.template import loader, TemplateDoesNotExist
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from irie.apps.events.models import Event
from irie.apps.site.view_utils import raise404
from irie.apps.inventory.models import Asset
from irie.apps.inventory.forms import AssetForm


@login_required(login_url="/login/")
def fetch_rendering(request):
    asset_id = request.GET.get('asset')
    asset = Asset.objects.get(id=asset_id)

    if asset.cesmd == "CE58658":
        template = loader.get_template(f"bridges/InteractiveTwin-{asset.cesmd}.html")
        return HttpResponse(template.render({}, request))


    from irie.apps.prediction.models import PredictorModel
    for p in PredictorModel.objects.filter(asset=asset):
        if p.protocol == "BRACE2_CLI_PREDICTOR_T4":
            return HttpResponse("html")

    return HttpResponse("No rendering available for this asset.")



def _make_freq_plot(evaluation):
    import numpy as np
    from mdof.macro import FrequencyContent

    plot = FrequencyContent(scale=True, period=True, xlabel="Period (s)", ylabel="Normalized Amplitude")

    for name, mdata in evaluation["summary"].items():
        periods = []
        amplitudes = []
        for i in mdata.get("data", []):
            if "period" in i:
                periods.append(i["period"])
                if "amplitude" in i:
                    amplitudes.append(i["amplitude"])

        if len(amplitudes) and (len(amplitudes) == len(periods)):
            plot.add(np.array(periods), np.array(amplitudes), label=name)
        else:
            plot.add(np.array(periods), label=name)

    fig = plot.get_figure()
    return fig.to_json()
 

@login_required(login_url="/login/")
def asset_event_summary(request, cesmd, event):
    from irie.apps.evaluation.models import Evaluation

    context = {}
    context["segment"] = "events"
    html_template = loader.get_template("inventory/asset-event-summary.html")

    try:

        segments = request.path.split("/")
        _, _, is_nce = segments[-3:]

        try:
            evaluation = Evaluation.objects.filter(event_id=int(event))[0]
            evaluation_data = evaluation.evaluation_data

        except Exception as e:
            # TODO: Handle case where evaluation cant be found
            evaluation_data = {}
            evaluation = None

        for metric in evaluation_data.values():
            metric["completion"] = (
                100 * len(metric["summary"])/len(metric["predictors"])
            )

        if "SPECTRAL_SHIFT_IDENTIFICATION" in evaluation_data:
            context["freq_plot_json"] = \
                    _make_freq_plot(evaluation_data["SPECTRAL_SHIFT_IDENTIFICATION"])

        context["all_evaluations"] = evaluation_data

        context["evaluation_details"] = { 
                 metric.replace("_", " ").title(): {
                    key:  [list(map(lambda i: f"{i:.3}" if isinstance(i,float) else str(i), row)) for row in table]
                    for key, table in predictors["details"].items()
                 } 
            for metric, predictors in sorted(evaluation_data.items(), key=lambda i: i[0])
        }
        context["asset"]       = evaluation and evaluation.event.asset or None
        context["nce_version"] = is_nce
        context["event_data"]  = Event.objects.get(pk=int(event)).motion_data


        resp = html_template.render(context, request)

        return HttpResponse(resp)

    except Exception as e:
        if "DEBUG" in os.environ and os.environ["DEBUG"]:
            raise e
        html_template = loader.get_template("site/page-500.html")
        return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def dashboard(request):
    from irie.apps.inventory.models import Asset
    from irie.apps.evaluation.models import Evaluation

    context = {}
    context["segment"] = "dashboard"
    try:
        if "demo" in request.path:
            context["demo_version"] = True

        context["recent_evaluations"] = [
            (evaluation, Event.objects.get(pk=evaluation.event_id))
            for evaluation in reversed(list(Evaluation.objects.all())[-6:])
        ]
        assets = [
            Asset.objects.get(cesmd=event[1].cesmd) for event in context["recent_evaluations"]
        ]
        context["asset_map"] = AssetMap(assets, 
                                        layer_assets=False, 
                                        traffic=False).get_html()
        context["calid"] = {b.cesmd: b.calid for b in assets}

        html_template = loader.get_template("inventory/dashboard.html")
        return HttpResponse(html_template.render(context, request))

    except Exception as e:
        if "DEBUG" in os.environ and os.environ["DEBUG"]:
            raise e
        html_template = loader.get_template("site/page-500.html")
        return HttpResponse(html_template.render(context, request))



def _ssid_stats(events, key):
    """
    mode_results is a list (station level) of lists (event level) of dictionaries (mode level).
    mode_results = [
        [
            {
                "period": ..., 
                "frequency": ...,
                "damping": ...,
                "emac": ...,
                "mpc": ...,
            },
            ...
        ],
        ...
    ]

    [
       # "Event"
       {"S1": {"period": [0.1]},
        "R1": {"period": [1.2]}}
    ]
    """
    mode_results = [_find_ssid(event.id) for event in events]
    import numpy as np

    filtered_results = [
            {
              method: [
                  result for result in event_results[method]
                        if key in result and result.get("emac", 1.0) > 0.5 and result.get("mpc", 1.0) > 0.5
              ] for method in event_results
            } for event_results in mode_results
    ]

    from collections import defaultdict
    values = defaultdict(list)
    for event in filtered_results:
        for method in event:
            for result in event[method]:
                values[method].append(result[key])

    mean = {method: np.mean(values[method]) for method in values}
    std =  {method: np.std(values[method]) for method in values}

    def _first(method_results):
        if method_results and len(method_results) > 0:
            results = np.array([result[key] for result in method_results])
            try:
                idx = np.argmax([result["amplitude"] for result in method_results])
                return results[idx]
            except KeyError:
                return np.max(results)
        else: 
            return {}

    return [
        {method: {
#           "distance": (closest_item[key]-mean)/std),
            "nearest_mean": event_results[method][np.argmin(np.abs(mean[method] \
                            - [result[key] for result in event_results[method]]))] \
                if event_results[method] and len(event_results[method]) > 0 else {} ,
            "maximum": _first(event_results[method])
            }
            for method in event_results
        }
        for event_results in filtered_results
    ]


def _find_ssid(event_id=None, evaluation=None):
    """
    Given an event ID, finds the results of the first configured
    system ID run. This generally looks like a list of dicts,
    each with fields "frequency", "damping", etc.
    """
    from irie.apps.evaluation.models import Evaluation

    if evaluation is None:
        evaluation = Evaluation.objects.filter(event_id=int(event_id))

    elif not isinstance(evaluation, list):
        evaluation = [evaluation]


    if len(evaluation) != 1:
        return []

    else:
        evaluation_data = evaluation[0].evaluation_data

    if "SPECTRAL_SHIFT_IDENTIFICATION" in evaluation_data:
        return {
                key: val.get("data", val.get("error", [])) 
                    for key,val in evaluation_data["SPECTRAL_SHIFT_IDENTIFICATION"]["summary"].items()
        }

    else:
        return []


@login_required(login_url="/login/")
def asset_profile(request, calid):

    context = {}
    html_template = loader.get_template("inventory/asset-profile.html")
    context["segment"] = "assets"

    context["nce_version"] = True

    try:
        asset = Asset.objects.get(calid=calid)

    except ObjectDoesNotExist:
        return raise404(request, context)

    context["asset"] = asset

    context["tables"] = _make_tables(asset)

    if asset.cesmd:
        cesmd = asset.cesmd

        events = list(reversed(sorted(Event.objects.filter(cesmd=cesmd),
                                      key=lambda x: x.motion_data["event_date"])))

        evals = [
            {"event": event,
             "pga": event.pga, #abs(event.motion_data["peak_accel"])/980., 
             "evaluation": ssid,
            }
            for i, (event, ssid) in enumerate(zip(events, _ssid_stats(events, "period")))
        ]
        context["evaluations"] = Paginator(evals, 5).get_page(1)

    try:
        return HttpResponse(html_template.render(context, request))

    # except TemplateDoesNotExist:
    #     context["rendering"] = None
    #     return HttpResponse(html_template.render(context, request))

    except Exception as e:
        if "DEBUG" in os.environ and os.environ["DEBUG"]:
            raise e
        html_template = loader.get_template("site/page-500.html")
        return HttpResponse(html_template.render(context, request))

def _make_tables(asset):
    if asset.cesmd:
        tables = [
        {k: v for k,v in group.items()
            if k not in {
                "Remarks",
                "Instrumentation",
                "Remarks/Notes",
                "Construction Date"
            }
        } for group in asset.cgs_data[1:]
        ]
    else:
        tables = []

    # Filter out un-interesting information
    nbi_data = [
      {k: v for k,v in group.items() 
           if k not in {
               "Owner Agency",
               "Year Reconstructed",
               "Bridge Posting Code",
               "Latitude",
               "Longitude",
               "NBIS Minimum Bridge Length",
               "Record Type",
               "State Name",
               "U.S. Congressional District",
               "Inventory Route NHS Code"
           }
       } for group in asset.nbi_data.values()
    ]
    tables.extend(nbi_data)
    tables = [tables[2], *tables[:2], *tables[3:]]
    condition = {}
    for table in tables:
        keys = set()
        for k in table:
            key = k.lower()
            if "condition" in key \
            or "rating" in key \
            or (re.search("^ *[0-9] - [A-Z]", table[k]) is not None and "code" not in key):
                condition[k] = table[k]
                keys.add(k)

        for k in keys:
            del table[k]

    tables.insert(3,condition)

    # for some tables, all values are empty. Filter these out
    tables = [
        table for table in tables if sum(map(lambda i: len(i),table.values()))
    ]
    return tables



@login_required(login_url="/login/")
def asset_table(request):
    """
    Returns a table of all assets in the database, paginated
    """

    context = {}
    context["segment"] = "assets"
    html_template = loader.get_template("inventory/asset-table.html")

    page = request.GET.get("page", 1)
    try:
        page = int(page)
    except:
        page = 1

    assets = Asset.objects.all() #exclude(cesmd__isnull=True),
    context["bridges"]   = Paginator(assets, 10).get_page(page)
    context["asset_map"] = AssetMap(assets=assets,
                                    cesmd=True, 
                                    layer_assets=True).get_html()

    try:
        return HttpResponse(html_template.render(context, request))

    except Exception as e:
        if "DEBUG" in os.environ and os.environ["DEBUG"]:
            raise e
        html_template = loader.get_template("site/page-500.html")
        return HttpResponse(html_template.render(context, request))



import folium
from folium import branca

class AssetMap:
    def __init__(self, 
                 assets, 
                 layer_assets=True, 
                 traffic=False, 
                 cesmd=True):
        self._layer_assets = layer_assets


        self._assets = assets

        self._figure = figure = folium.Figure()
        self._map    = m      = folium.Map(
            location=[37.7735, -122.0993], zoom_start=6, tiles=None
        )

        folium.raster_layers.TileLayer(
                tiles='cartodbpositron',
                name='Instrumented Bridges'
        ).add_to(m)
        m.add_to(figure)

        if cesmd:
            self.add_CESMD()

        if traffic:
            self.add_traffic()

        if self._layer_assets:

            self._asset_layers = {
                "partial":  folium.FeatureGroup(name="Partial Digital Twins"),
                "complete": folium.FeatureGroup(name="Full Digital Twins")
            }
            list(map(lambda i: i.add_to(self._map), self._asset_layers.values()))
            self.add_twins(list(self._asset_layers.values()))


    def get_html(self, **kwargs):
        folium.LayerControl(collapsed=False).add_to(self._map)
        self._figure.render()
        return self._map._repr_html_()

    def add_twins(self, features):

        for b in self._assets:
            lat, lon = b.coordinates
            popup = folium.Popup(
                        folium.Html(
                            '<a style="display: inline;" target="_blank" href="/inventory/{calid}/">{label}</a>'.format(
                                calid=b.calid,
                                label=b.calid
                            ), 
                            script=True
                        ),
                        min_width= 50,
                        max_width=100
            )
            if b.is_complete:
                folium.Marker(
                    location=[lat, lon],
                    popup=popup,
                    icon=folium.Icon(icon="cloud", color="blue" if not b.is_complete else "beige"),
                    z_index_offset=1000
                ).add_to(features[int(b.is_complete)])
            else:
                folium.CircleMarker(
                    location=[lat, lon],
                    popup=popup,
                    color="blue",
                    fill=True,
                    opacity=1,
                    fill_opacity=1,
                    radius=3,
                    z_index_offset=800
                ).add_to(features[int(b.is_complete)])
        return self

    def add_CESMD(self):
        cesmdbridges = folium.FeatureGroup(name="Registered Bridges")
        cesmdbridges.add_to(self._map)

        for b in self._assets:
            if not b.cesmd:
                continue
            lat, lon = b.coordinates

            folium.Marker(
                location=[lat, lon],
                popup=b.cesmd,
                icon=folium.Icon(icon="glyphicon-road", color="lightgray"),
            ).add_to(cesmdbridges)


    def add_traffic(self):
        # from irie.apps.inventory.traffic import TRAFFIC_LOW, TRAFFIC_MID, TRAFFIC_HIGH, TRAFFIC_ALL
        from irie.apps.inventory.traffic import TRAFFIC_ALL
        traffic = folium.FeatureGroup(name="Traffic")
        traffic.add_to(self._map)

        cm = branca.colormap.LinearColormap(colors=['green', 'yellow', 'orange', 'red'], vmin=10000, vmax=100000)
        for loc in TRAFFIC_ALL:
            folium.CircleMarker([loc["coords"][1],loc["coords"][0]],
                radius=5,
                popup=None,
                color=cm.rgb_hex_str(loc["properties"]["AHEAD_AADT"]),
                fill=True,
                opacity=0.5,
                weight=0,
               ).add_to(traffic)

        cm = branca.colormap.LinearColormap(colors=['green', 'yellow', 'orange', 'red'], 
                                            vmin=10000, vmax=100000, 
                                            caption='Average Annual Daily Traffic Crossings')
        cm.add_to(self._map)

        return self
