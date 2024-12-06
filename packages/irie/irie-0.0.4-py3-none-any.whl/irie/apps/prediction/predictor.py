#===----------------------------------------------------------------------===#
#
#         STAIRLab -- STructural Artificial Intelligence Laboratory
#
#===----------------------------------------------------------------------===#
#
#   This module implements the predictor abstraction.
#
#   Author: Claudio Perez
#
#----------------------------------------------------------------------------#
from __future__ import annotations
import sys
import json
import subprocess
from pathlib import Path
from typing import Dict

from .runners import Runner, RunID, Event, MetricType, classproperty, OpenSeesRunner



class PredictorType1(Runner):
    @property
    def platform(self):
        return self.conf.get("platform", "")

    @classmethod
    def create(cls, asset, request):
        from .models import PredictorModel
        predictor = PredictorModel()
        data = json.loads(request.data.get("json"))
        predictor.entry_point = [
            sys.executable, "-m", "opensees"
        ]
        data["metrics"] = []

        predictor.name = data.pop("name")
        predictor.config = data
        predictor.asset = asset
        predictor.protocol = "BRACE2_CLI_PREDICTOR_T1"
        predictor.active = False
        return predictor


    @classproperty
    def schema(cls):
        from .runners.opensees import schemas
        return {
            "title": "Structural Model",
            "options": {"disable_collaps": True},
            "schema": "http://json-schema.org/draft-04/schema#",
            "type": "object",
            "properties": {
                "platform": {
                  "type": "string",
                  "title": "Platform",
                  "enum": ["OpenSees","CSiBridge"]
                },
                "model":    schemas.load("hwd_conf.schema.json"),
                "analysis": schemas.load("hwd_analysis.schema.json"),
            }
        }

    def newPrediction(self, event: Event) -> RunID:
        self.event = event
        event_file = Path(event.event_file.path).resolve()
        command = [*self.entry_point, "new", event_file]
        run_id = subprocess.check_output(command).decode().strip()
        return RunID(int(run_id))

    def runPrediction(self, run_id: RunID):
        command = [*self.entry_point, "run", str(run_id)]

        if "scale" in self.event.upload_data:
            command.extend(["--scale", str(float(self.event.upload_data["scale"]))])
        print(":: Running ", command, file=sys.stderr)
        subprocess.check_output(command)

        print(f":: Model {self.name} returned", file=sys.stderr)
        return

    def getMetricData(self, run, metric):
        try:
            return json.loads(subprocess.check_output([*self.entry_point, "get", str(run), metric]).decode())
        except json.decoder.JSONDecodeError:
            return {}


class PredictorType2(Runner):
    platform = "mdof"

    schema = {
      "title": "System ID",
      "name": "P2",
      "type": "object",
      "required": [
        "name",
        "decimation",
        "method",
        "channels"
      ],
      "properties": {
        "name": {
          "type": "string",
          "title": "Name",
          "description": "Predictor name",
          "minLength": 2,
          # "default": "S1"
        },
        "method": {
          "type": "string",
          "title": "Method",
          "enum": ["Fourier Spectrum","Response Spectrum","SRIM","OKID"]
        },
        "decimation": {
          "type": "integer",
          "title": "Decimation",
          "default": 1,
          "minimum": 1,
          "maximum": 8
        },
        "order": {
          "type": "integer",
          "title": "Model Order",
          "default": 8,
          "minimum": 2,
          "maximum": 64,
          "options": {"dependencies": {"method": ["SRIM","OKID"]}}
        },
        "horizon": {
          "type": "integer",
          "title": "Prediction Horizon",
          "default": 100,
          "minimum": 50,
          "maximum": 500,
          "options": {"dependencies": {"method": ["SRIM"]}}
        },
        "period_band": {
          "type": "string",
          "title": "Period Band",
          "default": "[0.1,2.3]",
          "options": {"dependencies": {"method": ["Fourier Spectrum"]}},
          "description": "[0.1,2.3] if interested in periods between 0.1 seconds and 2.3 seconds"
        },
        "damping": {
          "type": "float",
          "title": "Damping",
          "default": 0.02,
          "options": {"dependencies": {"method": ["Response Spectrum"]}},
          "description": "assumed damping ratio"
        },
        "channels": {
          "type": "array",
          "format": "table",
          "title": "Channels",
          "uniqueItems": True,
          "items": {
            "title": "Acceleration",
            "type": "object",
            "properties": {
              "type": {
                "type": "string",
                "enum": ["output","input"],
                "default": "output"
              },
              "id": {"type": "integer", "description": "Number identifying signal channel"}
            }
          },
          "default": [{"type": "output", "id": 1}]
        }
      }
    }

    @classmethod
    def create(cls, asset, request):
        from .models import PredictorModel
        predictor = PredictorModel()
        data = json.loads(request.data.get("json"))
        method = {
                "Fourier Spectrum": "fourier",
                "Response Spectrum": "response",
                "FDD": "fdd",
                "OKID": "okid-era",
                "SRIM": "srim"
        }[data.pop("method")]
        predictor.entry_point = [
                sys.executable, "-m", "mdof", method
        ]
        data["outputs"] = [i["id"] for i in data["channels"] if i["type"] == "output"]
        data["inputs"]  = [i["id"] for i in data["channels"] if i["type"] == "input"]
        data["threads"] = 4
        data["metrics"] = ["SPECTRAL_SHIFT_IDENTIFICATION"]
        del data["channels"]

        predictor.name = data.pop("name")
        predictor.config = data
        predictor.asset = asset
        predictor.protocol = "BRACE2_CLI_PREDICTOR_T2"
        predictor.active = True
        return predictor


    def newPrediction(self, event):
        self.event = event
        return RunID(1)

    def runPrediction(self, run_id: RunID) -> bool:
        event_file = Path(self.event.event_file.path).resolve()
#       if "config" in self.conf:
        command = [*self.entry_point,
                   "--config", json.dumps(self.conf),
                   event_file]
        if False:
            command = [*self.entry_point,
                       event_file,
                       *map(str, self.conf.get("argv", []))]

        self.metric_details = subprocess.check_output(command).decode()
        print(self.metric_details)
        return True

    def getMetricData(self, run, metric):
        if not hasattr(self, "metric_details"):
            raise Exception(f"Error {self.name}({id(self)}), {run}")
        return json.loads(self.metric_details)


class PredictorType4(Runner):
    platform = "csi"

    schema = {
        "title": "CSI Predictor",
        "properties": {}
    }

    @classmethod
    def create(cls, asset, request, config):
        from .models import PredictorModel
        predictor = PredictorModel()

        predictor.entry_point = [
                sys.executable, "-m", "opensees"
        ]

        predictor.name = config.pop("name")
        predictor.config = config
        predictor.asset = asset
        predictor.protocol = "BRACE2_CLI_PREDICTOR_T4"
        predictor.active = True
        return predictor


    def newPrediction(self, event):
        self.event = event
        return RunID(1)

    def runPrediction(self, run_id: RunID) -> bool:
        event_file = Path(self.event.event_file.path).resolve()
#       if "config" in self.conf:
        command = [*self.entry_point,
                   "--config", json.dumps(self.conf),
                   event_file]
        if False:
            command = [*self.entry_point,
                       event_file,
                       *map(str, self.conf.get("argv", []))]

        self.metric_details = subprocess.check_output(command).decode()
        print(self.metric_details)
        return True

    def getMetricData(self, run, metric):
        if not hasattr(self, "metric_details"):
            raise Exception(f"Error {self.name}({id(self)}), {run}")
        return json.loads(self.metric_details)


PREDICTOR_TYPES : Dict[str, Runner] = {
    "BRACE2_CLI_PREDICTOR_V1" : PredictorType1,
    "BRACE2_CLI_PREDICTOR_T2" : PredictorType2,
    "" :                        PredictorType2,
#   "BRACE2_CLI_PREDICTOR_T3" : PredictorType3,
    "BRACE2_CLI_PREDICTOR_T4" : OpenSeesRunner,
}

