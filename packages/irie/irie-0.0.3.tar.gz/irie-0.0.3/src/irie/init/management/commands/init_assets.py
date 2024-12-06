"""
python manage.py shell < scripts/make_assets.py
"""
import irie
import lzma
import tarfile
from pathlib import Path
from django.core.management.base import BaseCommand
try:
    import orjson as json
except ImportError:
    import json

DATA = Path(irie.__file__).parents[0]/"init"/"data"

with open(DATA/"cgs_data.json") as f:
    CGS_DATA = json.loads(f.read())



from collections import defaultdict
from irie.apps.inventory.models  import Asset, Corridor
from irie.init.calid   import CALID, CESMD
from irie.init.bridges import BRIDGES

DRY = False
UPDATE_ASSETS = True

DISTRICTS = {
    # "01 - District 1",
    "04 - District 4",
    # "05 - District 5",
    # "06 - District 6",
    # "07 - District 7",
    # "08 - District 8",
    # "09 - District 9",
    # "11 - District 11",
    # "12 - District 12"
}

MIN_ADTT = 0 #  1_500
MIN_ADT  = 0 # 15_000

SKIP_DESIGN = {
    "19 - Culvert"
}

#-----------------------------------


def load_assets(NBI_DATA):
#   with open(NBI_FILE) as f:
#       NBI_DATA = json.loads(f.read())

    def find_bridge(bridges, calid):
        for bridge in bridges.values():
            if bridge["calid"].split(" ")[0] == calid:
                return bridge
        return {}

    def get_nbi(calid, missing_ok=False):
        data = defaultdict(dict)

        if missing_ok and calid not in NBI_DATA:
            return None

        blocks = NBI_DATA[calid]
        for row in blocks[-1]["Results"]["NBIData"]["NBIDataList"]:
            data[row["TABLE_NAME"]][row["EXPANDED_FIELD_ALIAS"]] = row["FIELD_VALUE"]

        return dict(data)


    def get_route(bridge):
        return "-".join(bridge["NBI_BRIDGE"]["Location"].split("-")[:3])


    def skip(bridge, routes):
        return not (
            (
                get_route(bridge) in routes
                and bridge["NBI_BRIDGE"]["Highway Agency District"] in DISTRICTS
#               and bridge["NBI_POSTING_STATUS"]["Structure Operational Status Code"] == "A - Open"
            ) or (
                bridge["NBI_BRIDGE"]["Highway Agency District"] in DISTRICTS
#               and bridge["NBI_BRIDGE"]["Type of Service on Bridge Code"] == "1 - Highway"
#               and bridge["NBI_BRIDGE"]["Owner Agency"] == "1 - State Highway Agency"
#               and bridge["NBI_SUPERSTRUCTURE_DECK"]["Main Span Design"] not in SKIP_DESIGN
#               and (
#                   "Concrete" in bridge["NBI_SUPERSTRUCTURE_DECK"]["Main Span Material"]
#                   or "Steel" in bridge["NBI_SUPERSTRUCTURE_DECK"]["Main Span Material"]
#               )
#               # and bridge["NBI_FEATURE"]["Inventory Route NHS Code"] == "1 - On NHS"
#               and int(bridge["NBI_FEATURE"]["Average Daily Truck Traffic (Volume)"]) >= MIN_ADTT
#               and int(bridge["NBI_FEATURE"]["Average Daily Traffic"]) >= MIN_ADT
                # and bridge["NBI_BRIDGE"]["Coulverts Condition Rating"] == "N - Not a culvert"
            )
        )


# 1. Collect routes of interest
    ROUTES = set()
    for bridge in BRIDGES.values():
        nbi = get_nbi(bridge["calid"].split(" ")[0].replace("-", " "), missing_ok=True)
        if nbi is not None:
            ROUTES.add(get_route(nbi))


    count = 0

#   CORRIDORS = defaultdict(set)

    for item in NBI_DATA:
        calid  = item.replace(" ", "-")
        nbi    = get_nbi(item)
        config = find_bridge(BRIDGES, calid)
        cesmd  = CESMD.get(calid, None)
        try:
            if skip(nbi, ROUTES) or item == "33 0726L":
                continue
        except:
            print("Failed to skip ", calid)
            continue

        count += 1
#       print(calid, f"({cesmd = })")

        cname = get_route(nbi)

#       CORRIDORS[cname].add(calid)


        if DRY:
            continue

        try:
            asset = Asset.objects.get(calid=calid)
            if UPDATE_ASSETS:
                if cesmd is not None:
                    asset.cesmd = cesmd
                asset.cgs_data = CGS_DATA.get(cesmd, {})
                asset.nbi_data = nbi
                asset.save()

#               print(">> Saved ", calid, f"({cesmd = })")

        except:
            if nbi is None:
                print(">> Skipping ", calid)
                continue

            name = config.get("name", nbi["NBI_BRIDGE"]["Location"])
            asset = Asset(cesmd=cesmd,
                      calid=calid,
                      name = name,
                      cgs_data = CGS_DATA.get(cesmd, {}),
                      nbi_data = nbi,
                      is_complete=False)
            asset.save()
            print(asset)

        continue


        try:
            corridor = Corridor.objects.get(name=cname)
            corridor.save()
            print(">> Saved ", cname)
            continue

        except:
            corridor = Corridor(name=cname)
            corridor.save()
            print(corridor)

        corridor.assets.add(asset)

        del nbi

    print(f"Created {count} of {len(NBI_DATA)} assets")

#   print(f"Created {len(CORRIDORS)} corridors")


class Command(BaseCommand):
    help = 'Description of what script_1 does'

    def handle(self, *args, **kwargs):
        # Open the tar file
        with tarfile.open(DATA/"04.tar", "r") as tar:
            # Iterate through each file in the tar archive
            for member in tar.getmembers():
                # Process only .xz files
                if member.name.endswith(".xz"):
                    print(f"Loading {member.name}...")

                    # Extract the xz-compressed file content
                    xz_file = tar.extractfile(member)

                    if xz_file is None:
                        print(f"Failed to extract {member.name}")
                        continue

                    # Decompress the .xz file
                    with lzma.LZMAFile(xz_file) as decompressed_file:
                        # Load the JSON content
                        try:
                            data = json.loads(decompressed_file.read())
                            load_assets(data)

                        except json.JSONDecodeError as e:
                            print(f"Failed to parse JSON in {member.name}: {e}")



#       NBI_FILE = data/"nbi_data-california.json" # os.environ.get("IRIE_INIT_ASSETS") # "data/nbi/04.json" #"nbi_data-500.json" # "data/nbi_data-california.json" # "data/nbi-california-2024.json" #  



