import os
import sys
import pathlib
import subprocess

from django.core.management import execute_from_command_line

cd = pathlib.Path(__file__).parents[0]

def init(settings):

    print("MIGRATING")
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings)
    execute_from_command_line([
        "__irie__",
        "migrate"
    ])


    with open(cd/"init_assets.py", "r") as f:
        result = subprocess.run([
            sys.executable, "-mirie.mgmt", "shell"
        ], stdin=f, capture_output=True, text=True)

if __name__ == "__main__":
    init(sys.argv[1])

