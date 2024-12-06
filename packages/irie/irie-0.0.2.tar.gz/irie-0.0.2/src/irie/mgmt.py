#!/usr/bin/env python
#===----------------------------------------------------------------------===#
#
#         STAIRLab -- STructural Artificial Intelligence Laboratory
#
#===----------------------------------------------------------------------===#

import os
import sys
from django.core.management import execute_from_command_line

def main():
#   os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'irie.core.settings')
#   print(sys.stdin.read())
    execute_from_command_line(sys.argv)
#   print(sys.argv)

if __name__ == '__main__':
    main()

