
from django.core.management.base import NoArgsCommand, BaseCommand

from django_noaa.models import Station

class Command(BaseCommand):
    help = "Imports station definitions."
    args = ''
    option_list = BaseCommand.option_list + (
    )
    
    def handle(self, **options):
        Station.load()
        