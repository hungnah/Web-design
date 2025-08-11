from django.core.management import call_command
import os

# Thiết lập môi trường Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tên_project.settings")

import django
django.setup()

with open("data.json", "w", encoding="utf-8") as f:
    call_command(
        "dumpdata",
        natural_primary=True,
        natural_foreign=True,
        indent=2,
        stdout=f
    )
