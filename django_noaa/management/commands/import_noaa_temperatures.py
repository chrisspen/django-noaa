from optparse import make_option

from django.core.management.base import NoArgsCommand, BaseCommand

from django_noaa.models import Station

class Command(BaseCommand):
    help = "Imports station temperatures."
    args = ''
    option_list = BaseCommand.option_list + (
        make_option('--force', action='store_true', default=False),
        make_option('--year', default=0),
    )
    
    def handle(self, **options):
        q = Station.objects.filter(load_temperatures=True).only('id')
        for station in q.iterator():
            print station
            station.load_temperature_records(
                force=options['force'],
                year=int(options['year']),
            )