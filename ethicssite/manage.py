#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import subprocess

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ethicssite.settings')
    # compiling typescript here
    try:
        print('compiling typescript...')
        subprocess.run(['tsc','-p','ethicssite/survey/scripts/tsconfig.json'])
        print('compilation successful!')
    except: print('typescript compile failed!')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
