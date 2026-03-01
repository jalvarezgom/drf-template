from django.core.management import BaseCommand


class Command(BaseCommand):
    help = "Staff maintenance command"
    STAFF_OPTIONS = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_arguments(self, parser):
        parser.add_argument(
            "--option",
            help="Select the seeder to run",
        )

    def handle(self, *args, **options):
        print("Inicio - CMD STAFF.PY")
        user_option = options.get("option")
        if not user_option:
            print("What actions are going to run?")
            for idx, seeder in enumerate(self.STAFF_OPTIONS):
                print(f"{idx + 1}. {seeder.__name__}")
            print("99. All")
            user_option = input("Select an option: ")
        if user_option == "99":
            for seeder in self.STAFF_OPTIONS:
                seeder.run()
        else:
            try:
                user_option = int(user_option)
                seeder = self.STAFF_OPTIONS[user_option - 1]
                print(f"STAFF - Running {seeder.__name__}")
                seeder.run()
            except IndexError:
                print("Invalid option")
        print("Fin - CMD STAFF.PY")
