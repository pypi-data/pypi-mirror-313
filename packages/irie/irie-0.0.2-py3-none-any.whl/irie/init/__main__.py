import os
import sys
import pathlib
import subprocess

from django.core.management import execute_from_command_line, call_command

cd = pathlib.Path(__file__).parents[0]

def init(settings):

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings)

    execute_from_command_line([
        "__irie__",
        "migrate"
    ])

    call_command("makemigrations")

    call_command("migrate")

    call_command("init_assets")

    call_command("init_corridors")



if __name__ == "__main__":
    init(sys.argv[1])

