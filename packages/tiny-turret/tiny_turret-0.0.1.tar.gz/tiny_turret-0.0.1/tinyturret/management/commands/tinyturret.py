from django.core.management.base import BaseCommand

from tinyturret import cli


class Command(BaseCommand):

    def add_arguments(self, parser):
        cli.add_arguments(parser)

    def handle(self, *args, **options):
        Options = type("Options", (), {})
        option_attrs = Options()
        for k, v in options.items():
            setattr(option_attrs, k, v)
        cli.run_main(option_attrs)
