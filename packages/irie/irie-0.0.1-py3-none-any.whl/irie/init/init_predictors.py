"""
Assets must already be created
"""

import json

from irie.apps.inventory.models import Asset
from irie.apps.prediction.models  import PredictorModel
from init.bridges import BRIDGES

for bridge in BRIDGES.values():
    print(bridge["cesmd"])
    for conf in bridge.get("predictors", []):
        print(">> ", conf["name"])
        try:
            "a" + 1
            pred = PredictorModel.objects.get(cesmd=bridge["cesmd"])
            pred.config = conf["config"]
            pred.name   = conf["name"]
            pred.save()

            print(">> Saved ", bridge["cesmd"])
            continue
        except:
            protocol = PredictorModel.Protocol.TYPE2
            for type in PredictorModel.Protocol:
                print(f"  {type._name_}:  {conf['protocol']}")
                if str(type) == conf["protocol"]:
                    protocol = type

#           if protocol is None:
#               raise ValueError(f"Unknown predictor protocol: {conf['protocol']}")
            config = conf.get("config", {})

            a = PredictorModel(asset  = Asset.objects.get(cesmd=bridge["cesmd"]),
                               name   = conf["name"],
                               entry_point   = conf["entry_point"],
                               config = config,
                               description = conf.get("description", ""),
                               active = True,
                               metrics = list(conf.get("metrics", [])),
                               protocol = protocol
                               )
            a.save()
            print(a)

