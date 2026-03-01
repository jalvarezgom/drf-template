from django.core.management import BaseCommand


class Command(BaseCommand):
    help = "TODO"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        print("INICIO - CMD_TEST.PY")

        print("FIN - CMD_TEST.PY")
