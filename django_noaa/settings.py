from django.conf import settings

STATIONS_URL = settings.NOAA_STATIONS_URL = getattr(
    settings,
    'NOAA_STATIONS_URL',
    'http://www1.ncdc.noaa.gov/pub/data/uscrn/products/stations.tsv')

HOURLY_TEMPERATURE_URL = settings.NOAA_HOURLY_TEMPERATURE_URL = getattr(
    settings,
    'NOAA_HOURLY_TEMPERATURE_URL',
    'http://www1.ncdc.noaa.gov/pub/data/uscrn/products/hourly02/{year:04d}/CRNH02{file_format:02d}-{year:04d}-{state}_{location}_{vector}.txt')
