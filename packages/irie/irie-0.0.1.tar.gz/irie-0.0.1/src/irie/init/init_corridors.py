"""
To run:
  python manage.py shell < scripts/init_corridors.py

This script depends on the files:
    soga_corridors.json

This file is created using the script make_corridors.py
which takes in corridor_line.geojson and soga_corridors.csv
"""

import sys
import csv
import json
from collections import defaultdict
from irie.apps.inventory.models   import Asset, Corridor

if True:
    with open("data/soga_corridors.json") as f:
        corridors = json.load(f)

    for cdata in corridors:
        cname = cdata["name"]

        try:
            corridor = Corridor.objects.get(name=cname)

        except:
            corridor = Corridor(name=cname)

        for calid in cdata["bridges"]:
            # corridor.assets.add(Asset.objects.get(calid=calid))
            try:
                corridor.assets.add(Asset.objects.get(calid=calid))
                print(f"Added {calid} to {corridor.name}")
            except Exception as e:
                print(f"Failed to find assed with calid {calid} ({e})")

        corridor.save()
