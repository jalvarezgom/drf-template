from django.core.management import BaseCommand


class Command(BaseCommand):
    help = "TODO"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        print("Inicio - CMD TESTS.PY")
        func = print
        print(f"func: {func}")
        input("Press Enter to continue...")
        func()
        print("Fin - CMD TESTS.PY")
