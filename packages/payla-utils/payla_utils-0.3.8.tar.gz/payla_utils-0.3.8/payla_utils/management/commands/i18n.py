# ruff: noqa: S603,S607

import subprocess
from io import StringIO

from django.core.management import BaseCommand, call_command


class Command(BaseCommand):
    help = "Make and compile messages for german language"
    requires_system_checks: list = []

    def handle(self, *args, **options):
        self.stdout.write("Making messages", style_func=self.style.SUCCESS)
        out = StringIO()
        call_command(
            "makemessages",
            locale=["de"],
            no_location=True,
            no_obsolete=True,
            extension=["html", "py", "txt", "js", "tpl"],
            stdout=out,
        )

        self.stdout.write(out.getvalue())

        # remove POT-Creation-Date from all .po files using sed
        subprocess.call(["find", ".", "-name", "*.po", "-exec", "sed", "-i", "-e", "/POT-Creation-Date/d", "{}", ";"])

        self.stdout.write("Compiling messages", style_func=self.style.SUCCESS)
        call_command("compilemessages", locale=["de"])
