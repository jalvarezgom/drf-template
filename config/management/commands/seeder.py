from django.core.management import BaseCommand


class Command(BaseCommand):
    help = "Seeding database with initial data"
    SEEDER_OPTIONS = [
        # SeederStaticData,
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_arguments(self, parser):
        parser.add_argument(
            "--option",
            help="Select the seeder to run",
        )

    def handle(self, *args, **options):
        print("Inicio - CMD SEEDER.PY")
        user_option = options.get("option")
        if not user_option:
            print("What seeders are going to run?")
            for idx, seeder in enumerate(self.SEEDER_OPTIONS):
                print(f"{idx + 1}. {seeder.__name__}")
            print("99. All")
            user_option = input("Select an option: ")
        if user_option == "99":
            for seeder in self.SEEDER_OPTIONS:
                seeder.run()
        else:
            try:
                user_option = int(user_option)
                seeder = self.SEEDER_OPTIONS[user_option - 1]
                print(f"SEEDER - Running {seeder.__name__}")
                seeder.run()
            except IndexError:
                print("Invalid option")
        print("Fin - CMD SEEDER.PY")
