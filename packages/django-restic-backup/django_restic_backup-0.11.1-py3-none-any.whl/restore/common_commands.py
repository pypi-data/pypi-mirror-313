from abc import ABCMeta

from django.core.management import BaseCommand, CommandError


class CommonCommand(BaseCommand, metaclass=ABCMeta):
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    DARKCYAN = "\033[36m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"

    def _write(self, msg, no_ending, stdout=None):
        if stdout is None:
            stdout = self.stdout

        if no_ending:
            stdout.write(msg, ending="")
        else:
            stdout.write(msg)

    def info(self, msg, no_ending=False):
        self._write(self.style.MIGRATE_HEADING(msg), no_ending)

    def success(self, msg, no_ending=False):
        self._write(self.style.SUCCESS(msg), no_ending)

    def warning(self, msg, no_ending=False):
        self._write(self.style.WARNING(msg), no_ending)

    def error(self, msg, no_ending=False):
        self._write(self.style.ERROR(msg), no_ending, stdout=self.stderr)


class DealIdCommand(CommonCommand):
    """Add a deal_id argument and validate it."""

    def add_arguments(self, parser):
        parser.add_argument("deal_id", type=str, help="Deal id")

    def handle(self, *agrs, **options):
        deal_id = options["deal_id"]
        from deals.models import Deal

        try:
            self.deal = Deal.objects.get(id=deal_id)
        except Deal.DoesNotExist:
            raise CommandError(f"Deal '{deal_id}' does not exist.")
